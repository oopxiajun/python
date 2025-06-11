"""
V3  版本：
修复问题：
1：展示历史诊断记录，支持多轮问答
2：门店推荐

使用DeepSeek LLM进行信息提取、诊断、决策和门店推荐
智能汽车故障诊断助手
这是一个基于Streamlit的智能汽车故障诊断应用，使用DeepSeek LLM进行信息提取、诊断、决策和门店推荐。用户可以输入车牌号和车辆问题描述，系统将自动提取车辆信息，进行故障诊断，并推荐合适的维修店。
"""
import streamlit as st
from langchain.chains import SequentialChain, TransformChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from deepseek_llm import DeepSeekLLM
from dotenv import load_dotenv 

load_dotenv()

import json
import datetime
import random
import os
import re

# 初始化DeepSeek LLM
api_key = os.getenv("DEEPSEEK_API_KEY")  
llm = DeepSeekLLM(api_key=api_key, temperature=0.3, max_tokens=1500)

# 模拟车辆数据库
VEHICLE_DB = {
    "川A12345": {
        "brand": "Toyota",
        "model": "Camry",
        "year": 2023,
        "mileage": 45000,
        "last_service": "2023-12-15",
        "insurance_expiry": "2025-09-30",
        "next_maintenance": "2026-06-30"
    },
    "川B67890": {
        "brand": "Honda",
        "model": "CR-V",
        "year": 2019,
        "mileage": 60000,
        "last_service": "2024-11-20",
        "insurance_expiry": "2025-08-15",
        "next_maintenance": "2026-05-20"
    }
}

# 模拟维修店数据库
REPAIR_SHOPS = [
    {"id": 1, "name": "诚信汽修", "distance": "1.2km", "rating": 4.8, 
     "services": ["机油更换", "刹车维修", "发动机诊断", "轮胎更换", "保养套餐", "电子诊断", "快速保养", "玻璃水加注", "简单维修", "空调维修", "电瓶更换", "变速箱维修", "悬挂系统检查", "灯光维修", "喷漆服务"], "price_level": "$$"},
    {"id": 2, "name": "途虎养车工场店", "distance": "2.3km", "rating": 4.7, 
     "services": ["轮胎更换", "保养套餐", "电子诊断", "机油更换", "刹车维修", "发动机诊断", "空调维修", "电瓶更换", "变速箱维修", "悬挂系统检查", "灯光维修", "喷漆服务", "快速保养", "玻璃水加注", "简单维修"], "price_level": "$$$"},
    {"id": 3, "name": "小李快修", "distance": "0.8km", "rating": 4.5, 
     "services": ["快速保养", "玻璃水加注", "简单维修", "机油更换", "刹车维修", "轮胎更换", "空调维修", "电瓶更换", "发动机诊断", "灯光维修", "喷漆服务"], "price_level": "$"},
    {"id": 4, "name": "点点修车", "distance": "8km", "rating": 5.0, 
     "services": ["维修保养", "玻璃水加注", "简单维修", "机油更换", "刹车维修", "轮胎更换", "发动机诊断", "空调维修", "电瓶更换", "变速箱维修", "悬挂系统检查", "灯光维修", "喷漆服务", "保养套餐", "电子诊断"], "price_level": "$$$$"}
]

# 模拟知识库音频
SOUND_LIBRARY = {
    "哒哒声": "https://www.auto11.com/sound/ticking.mp3",
    "嗡嗡声": "https://www.auto11.com/sound/humming.mp3",
    "吱吱声": "https://www.auto11.com/sound/squeaking.mp3",
    "咔嗒声": "https://www.auto11.com/sound/clicking.mp3"
}

# 1. 信息提取链
def extract_vehicle_info(inputs: dict) -> dict:
    license_plate = inputs["license_plate"]
    vehicle_info = VEHICLE_DB.get(license_plate, {})
    
    if not vehicle_info:
        st.error(f"未找到车牌号 {license_plate} 的车辆信息")
        return {"vehicle_info": "未知车辆"}
    
    # 检查服务提醒
    today = datetime.date.today()
    reminders = []
    
    insurance_expiry = datetime.datetime.strptime(vehicle_info["insurance_expiry"], "%Y-%m-%d").date()
    if (insurance_expiry - today).days < 30:
        reminders.append({"type": "insurance", "message": "您的车辆保险即将到期"})
    
    next_maintenance = datetime.datetime.strptime(vehicle_info["next_maintenance"], "%Y-%m-%d").date()
    if (next_maintenance - today).days < 30:
        reminders.append({"type": "maintenance", "message": "您的车辆即将需要保养"})
    
    return {
        "vehicle_info": json.dumps(vehicle_info),
        "reminders": json.dumps(reminders)
    }

info_extraction_chain = TransformChain(
    input_variables=["license_plate"],
    output_variables=["vehicle_info", "reminders"],
    transform=extract_vehicle_info
)

# 2. 诊断链
def setup_diagnosis_chain():
    diagnosis_template = """
    您是一名专业的汽车维修技师，正在帮助车主诊断车辆问题。请根据以下信息进行诊断：
    
    车辆信息：{vehicle_info}
    用户描述的症状：{symptoms}
    
    请根据您的专业知识：
    1. 分析可能的故障原因
    2. 生成最多3个关键问题来进一步明确问题
    3. 对于异响类问题，请建议用户试听哪种声音样本
    
    输出格式：
    {{
        "analysis": "对问题的初步分析",
        "questions": ["问题1", "问题2", "问题3"],
        "sound_suggestion": "建议试听的声音类型"
    }}
    """
    
    prompt = PromptTemplate(
        template=diagnosis_template,
        input_variables=["vehicle_info", "symptoms"]
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="diagnosis_result")
    # 使用带错误处理的链
    # chain = LLMChain(llm=llm, prompt=prompt, output_key="diagnosis_result")
    
    # def safe_chain(inputs):
    #     try:
    #         return chain(inputs)
    #     except Exception as e:
    #         st.error(f"诊断过程中出错: {str(e)}")
    #         return {
    #             "diagnosis_result": json.dumps({
    #                 "analysis": "无法完成诊断",
    #                 "questions": [],
    #                 "sound_suggestion": None
    #             })
    #         }
    
    # return safe_chain
# 3. 维修决策链
def setup_repair_decision_chain():
    decision_template = """
    基于以下诊断信息：
    {diagnosis_result}
    
    请判断：
    1. 车主是否能够自行修复问题？（是/否）
    2. 如果可自行修复，提供详细的步骤指导
    3. 如果需要专业维修，推荐维修项目
    
    输出格式：
    {{
        "self_repairable": true/false,
        "repair_steps": ["步骤1", "步骤2", ...],
        "recommended_services": ["服务1", "服务2", ...]
    }}
    """
    
    prompt = PromptTemplate(
        template=decision_template,
        input_variables=["diagnosis_result"]
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="repair_decision")

# 4. 门店推荐链
def recommend_shops(inputs: dict) -> dict:
    decision = json.loads(inputs["repair_decision"])
    print("------------------维修决策   ", decision)
    # if decision.get("self_repairable", False) is False:
    #     return {"shop_recommendations": json.dumps([])}
    
    # 根据位置和推荐服务筛选门店
    location = inputs["location"]
    recommended_services = decision.get("recommended_services", [])
    print("自定义维修服务   ", recommended_services)
    filtered_shops = []

    # 将推荐服务拆分为单个字符集合
    def extract_keywords(service):
        # 只保留中文和英文字符
        return set(re.findall(r'[\u4e00-\u9fa5a-zA-Z]', service))

    recommended_keywords = set()
    for service in recommended_services:
        recommended_keywords |= extract_keywords(service)

    for shop in REPAIR_SHOPS:
        # 将门店服务也拆分为关键词集合
        shop_keywords = set()
        for s in shop["services"]:
            shop_keywords |= extract_keywords(s)
        # 模糊匹配：只要有交集就算匹配
        if recommended_keywords & shop_keywords:
            shop["match_score"] = random.uniform(0.7, 1.0)  # 模拟匹配度计算
            filtered_shops.append(shop)
    
    # 按距离和评分排序
    filtered_shops.sort(key=lambda x: (x["distance"], -x["rating"]))
    print("=======筛选后的维修店：", filtered_shops)
    return {"shop_recommendations": json.dumps(filtered_shops[:3])}

shop_recommendation_chain = TransformChain(
    input_variables=["repair_decision", "location"],
    output_variables=["shop_recommendations"],
    transform=recommend_shops
)

# 完整工作流
def create_full_workflow():
    diagnosis_chain = setup_diagnosis_chain()
    repair_decision_chain = setup_repair_decision_chain()
    
    return SequentialChain(
        chains=[
            info_extraction_chain,
            diagnosis_chain,
            repair_decision_chain,
            shop_recommendation_chain
        ],
        input_variables=["license_plate", "symptoms", "location"],
        output_variables=["vehicle_info", "reminders", "diagnosis_result", 
                          "repair_decision", "shop_recommendations"],
        verbose=True
    )

# Streamlit UI
def main():
    st.set_page_config(page_title="智能汽车故障诊断", layout="wide")
    st.title("🚗 汽车故障诊断——智能助手")
    
    # 初始化session状态
    if "diagnosis_stage" not in st.session_state:
        st.session_state.diagnosis_stage = "initial"
        st.session_state.memory = ConversationBufferMemory()
        st.session_state.workflow = create_full_workflow()
        st.session_state.answers = {}
        # st.session_state.current_questions = []
        st.session_state.diagnosis_history = []  # 新增：存储历史诊断记录**
    
    # 侧边栏 - 车辆信息输入
    with st.sidebar:
        st.header("车辆信息")
        license_plate = st.text_input("车牌号", "川A12345")
        location = st.text_input("当前位置", "成都市武侯区天泰路")
        
        st.header("车辆状态")
        if license_plate in VEHICLE_DB:
            vehicle = VEHICLE_DB[license_plate]
            st.write(f"品牌: {vehicle['brand']}")
            st.write(f"型号: {vehicle['model']}")
            st.write(f"里程: {vehicle['mileage']}公里")
            st.write(f"上次保养: {vehicle['last_service']}")
            
            # 服务提醒
            today = datetime.date.today()
            insurance_expiry = datetime.datetime.strptime(vehicle["insurance_expiry"], "%Y-%m-%d").date()
            days_to_expiry = (insurance_expiry - today).days
            if days_to_expiry < 0:
                # 已过期，计算过期了多久
                overdue_days = abs(days_to_expiry)
                years = overdue_days // 365
                months = (overdue_days % 365) // 30
                days = (overdue_days % 365) % 30
                st.error(f"⛔ 保险已于 {overdue_days} 天前过期（到期日: {vehicle['insurance_expiry']}）")
            elif days_to_expiry < 300:
                st.warning(f"⏰ 保险将于 {vehicle['insurance_expiry']} 到期")
            
            next_maintenance = datetime.datetime.strptime(vehicle["next_maintenance"], "%Y-%m-%d").date()
            if (next_maintenance - today).days < 300:
                st.warning(f"🔧 下次保养时间: {vehicle['next_maintenance']}")
    
    # 主界面 - 诊断流程
    if st.session_state.diagnosis_stage == "initial":
        st.subheader("请描述您的车辆问题")
                # 使用st.text_area的key参数和session_state来跟踪文本内容
        if 'symptoms_text' not in st.session_state:
            st.session_state.symptoms_text = ""
        
        # 创建文本输入区域
        symptoms = st.text_area(
            "例如：冷启动时有哒哒异响，仪表盘机油灯闪烁",
            value=st.session_state.symptoms_text,
            height=150,
            key="symptoms_input",
            help="按Enter键提交，Ctrl+Enter换行"
        )
        
        # 监听键盘事件
        if st.session_state.get('symptoms_input_last_value', '') != symptoms:
            st.session_state.symptoms_text = symptoms
            st.session_state.symptoms_input_last_value = symptoms
            
            # 检查是否按下了Enter键（无Ctrl）
            if '\n' in symptoms and not st.session_state.get('ctrl_pressed', False):
                # 移除最后一个换行符（由Enter键产生）
                cleaned_symptoms = symptoms.rsplit('\n', 1)[0]
                st.session_state.symptoms_text = cleaned_symptoms
                
                if cleaned_symptoms.strip():
                    # 自动触发诊断
                    st.session_state.symptoms = cleaned_symptoms
                    st.session_state.license_plate = license_plate
                    st.session_state.location = location
                    st.session_state.diagnosis_stage = "processing"
                    st.rerun()
                else:
                    st.error("请输入车辆问题描述")
        
        # 添加JavaScript检测Ctrl+Enter
        st.components.v1.html("""
        <script>
        const textarea = document.querySelector("textarea[data-testid='stTextArea']");
        if (textarea) {
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    // 标记Ctrl+Enter被按下
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        key: 'ctrl_enter_pressed',
                        value: true
                    }, '*');
                }
            });
        }
        </script>
        """, height=0)
        
        # 处理JavaScript消息
        if st.session_state.get('ctrl_enter_pressed'):
            st.session_state.ctrl_pressed = True
            st.session_state.ctrl_enter_pressed = False
        else:
            st.session_state.ctrl_pressed = False
        
        # 保留手动提交按钮作为备选方案
        if st.button("开始诊断"):
            if not st.session_state.symptoms_text.strip():
                st.error("请输入车辆问题描述")
                return
                
            st.session_state.symptoms = st.session_state.symptoms_text
            st.session_state.license_plate = license_plate
            st.session_state.location = location
            st.session_state.diagnosis_stage = "processing"
            st.rerun()
    
    # 诊断处理中
    elif st.session_state.diagnosis_stage == "processing":
        # 先显示历史记录
        if st.session_state.diagnosis_history:
            st.subheader("📝 诊断历史记录")
            for i, entry in enumerate(st.session_state.diagnosis_history, 1):
                with st.expander(f"诊断轮次 {i}", expanded=True):
                    if entry["stage"] == "question_answers":
                        st.markdown("**问题与回答:**")
                        for q, a in zip(entry["questions"], entry["answers"]):
                            st.markdown(f"- **问:** {q}")
                            st.markdown(f"  **答:** {a}")
                    elif entry.get("diagnosis_result"):
                        st.markdown("**诊断分析:**")
                        st.write(entry["diagnosis_result"]["analysis"])
                        if "sound_suggestion" in entry["diagnosis_result"]:
                            st.audio(SOUND_LIBRARY.get(entry["diagnosis_result"]["sound_suggestion"]))
        print("----1---")
        with st.spinner("正在分析您的车辆问题..."):
            print("----1.1---")
            try:
                result = st.session_state.workflow({
                    "license_plate": st.session_state.license_plate,
                    "symptoms": st.session_state.symptoms,
                    "location": st.session_state.location
                })
                print("----2---",result)
                # 添加结果验证
                if not result.get("diagnosis_result"):
                    raise ValueError("诊断结果为空")
                    
                diagnosis_result = json.loads(result["diagnosis_result"])
                
                # 验证必要字段
                required_fields = ["analysis", "questions"]
                for field in required_fields:
                    if field not in diagnosis_result:
                        raise ValueError(f"诊断结果缺少必要字段: {field}")
                        
                # 存储结果...

            # try:
            #     print(f"License Plate: {st.session_state.license_plate}")
            #     print(f"Symptoms: {st.session_state.symptoms}")
            #     print(f"Location: {st.session_state.location}")

            #     # 执行工作流
            #     result = st.session_state.workflow({
            #         "license_plate": st.session_state.license_plate,
            #         "symptoms": st.session_state.symptoms,
            #         "location": st.session_state.location
            #     })
            #     print("执行工作流：",result)
                # 解析结果
                # = json.loads(result.get["diagnosis_result"])
                repair_decision = json.loads(result["repair_decision"])
                shop_recommendations = json.loads(result["shop_recommendations"])
                
                history_entry = {
                    "stage": "diagnosis",
                    "diagnosis_result": diagnosis_result,
                    "repair_decision": repair_decision,
                    "shop_recommendations": shop_recommendations
                }
                st.session_state.diagnosis_history.append(history_entry)  # 保存完整诊断结果
                


                # 存储结果
                st.session_state.diagnosis_result = diagnosis_result
                st.session_state.repair_decision = repair_decision
                st.session_state.shop_recommendations = shop_recommendations
                st.session_state.current_questions = diagnosis_result.get("questions", [])
                
                # 如果有声音建议，准备音频
                sound_type = diagnosis_result.get("sound_suggestion")
                if sound_type and sound_type in SOUND_LIBRARY and SOUND_LIBRARY[sound_type]:
                    st.session_state.sound_url = SOUND_LIBRARY[sound_type]
                else:
                    st.session_state.sound_url = None
                
                st.session_state.diagnosis_stage = "show_results"
                st.rerun()
                
            except Exception as e:
                print(e)
                st.error(f"诊断过程中发生错误: {str(e)}")
                st.session_state.diagnosis_stage = "initial"                            
            except json.JSONDecodeError as e:
                st.error("诊断结果解析失败，请重试")
                st.session_state.diagnosis_stage = "initial"
            except Exception as e:
                st.error(f"诊断失败: {str(e)}")
                st.session_state.diagnosis_stage = "initial"
            finally:
                st.rerun()
    
    # 显示诊断结果
    elif st.session_state.diagnosis_stage == "show_results":       
        # 始终显示完整历史记录
        if st.session_state.diagnosis_history:
            st.subheader("📝 完整诊断历史")
            for i, entry in enumerate(st.session_state.diagnosis_history, 1):
                with st.expander(f"诊断轮次 {i}", expanded=True):
                    if entry["stage"] == "question_answers":
                        st.markdown("**问题与回答:**")
                        for q, a in zip(entry["questions"], entry["answers"]):
                            st.markdown(f"- **问:** {q}")
                            st.markdown(f"  **答:** {a}")
                    elif entry.get("diagnosis_result"):
                        st.markdown("**诊断分析:**")
                        st.write(entry["diagnosis_result"]["analysis"])
                        if "sound_suggestion" in entry["diagnosis_result"]:
                            st.audio(SOUND_LIBRARY.get(entry["diagnosis_result"]["sound_suggestion"]))
        
        # 显示当前诊断结果
        st.subheader("🔍 最新诊断结果")
        
        # 显示初步分析
        st.markdown(f"**问题分析:** {st.session_state.diagnosis_result.get('analysis', '')}")
        
        # 播放声音建议
        if st.session_state.sound_url:
            st.markdown("**声音对比:** 请听以下声音是否与您的车辆声音相似")
            st.audio(st.session_state.sound_url, format='audio/mp3')
        
        # 显示进一步问题
        if st.session_state.current_questions:
            st.markdown("**请回答以下问题以进一步明确问题:**")
            for i, question in enumerate(st.session_state.current_questions):
                st.session_state.answers[i] = st.text_input(question, key=f"q_{i}")
            
            if st.button("提交答案并继续诊断"):
                # **保存历史记录**
                history_entry = {
                    "stage": "question_answers",
                    "questions": st.session_state.current_questions,
                    "answers": list(st.session_state.answers.values())
                }
                st.session_state.diagnosis_history.append(history_entry)

                # 将答案添加到症状描述中
                new_symptoms = "\n".join([f"Q: {st.session_state.current_questions[i]}\nA: {st.session_state.answers[i]}" 
                                         for i in range(len(st.session_state.current_questions))])
                st.session_state.symptoms += "\n" + new_symptoms

                # **重置当前问题，触发重新诊断**
                #st.session_state.current_questions = []  # 清空当前问题
                st.session_state.diagnosis_stage = "processing"
                st.rerun()
        
        # 显示维修决策
        st.divider()
        decision = st.session_state.repair_decision
        
        if decision.get("self_repairable", False):
            st.success("✅ 您可以尝试自行修复此问题")
            st.markdown("**修复步骤:**")
            for i, step in enumerate(decision.get("repair_steps", [])):
                st.markdown(f"{i+1}. {step}")
            
            # 添加AR指导按钮
            if st.button("查看AR修复指导"):
                st.session_state.show_ar = True
                
            if st.session_state.get("show_ar", False):
                st.video("https://example.com/ar_repair_guide.mp4")
        else:
            st.warning("⚠️ 建议到专业维修店处理此问题")
            st.markdown(f"**推荐维修项目:** {', '.join(decision.get('recommended_services', []))}")
            
            # 显示推荐门店
            st.subheader("推荐维修店")
            if st.session_state.shop_recommendations:
                cols = st.columns(len(st.session_state.shop_recommendations))
                for i, shop in enumerate(st.session_state.shop_recommendations):
                    with cols[i]:
                        st.markdown(f"**{shop['name']}**")
                        st.caption(f"距离: {shop['distance']} | 评分: {shop['rating']}")
                        st.caption(f"服务: {', '.join(shop['services'][:3])}")
                        st.caption(f"价格: {shop['price_level']}")
                        
                        if st.button("选择此门店", key=f"shop_{i}"):
                            st.session_state.selected_shop = shop
                            st.session_state.diagnosis_stage = "shop_selected"
                            st.rerun()
            else:
                st.info("未找到匹配的维修店，请尝试扩大搜索范围")
        
        # 返回按钮
        if st.button("重新诊断"):
            st.session_state.diagnosis_stage = "initial"
            st.rerun()
    
    # 门店选择后
    elif st.session_state.diagnosis_stage == "shop_selected":
        shop = st.session_state.selected_shop
        st.success(f"您已选择: {shop['name']}")
        
        # 显示预约信息
        st.subheader("预约信息")
        date = st.date_input("预约日期", min_value=datetime.date.today())
        time = st.time_input("预约时间", datetime.time(10, 00))
        contact = st.text_input("联系电话")
        
        # 维修项目确认
        st.subheader("维修项目确认")
        services = st.session_state.repair_decision.get("recommended_services", [])
        selected_services = st.multiselect("请确认维修项目", services, default=services)
        
        if st.button("确认预约"):
            st.session_state.appointment = {
                "shop": shop["name"],
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M"),
                "services": selected_services,
                "contact": contact
            }
            st.session_state.diagnosis_stage = "appointment_confirmed"
            st.rerun()
    
    # 预约确认
    elif st.session_state.diagnosis_stage == "appointment_confirmed":
        appt = st.session_state.appointment
        st.balloons()
        st.success("🎉 预约成功！")
        
        st.markdown(f"""
        **维修店:** {appt['shop']}  
        **时间:** {appt['date']} {appt['time']}  
        **维修项目:** {', '.join(appt['services'])}  
        **联系电话:** {appt['contact']}
        """)
        
        st.info("维修店将很快联系您确认预约详情")
        
        if st.button("返回主页"):
            st.session_state.diagnosis_stage = "initial"
            st.rerun()

if __name__ == "__main__":
    main()