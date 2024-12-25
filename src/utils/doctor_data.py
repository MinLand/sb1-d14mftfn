from models.doctor_knowledge import DoctorKnowledge

DOCTOR_DATA = {
    "赵医生": DoctorKnowledge(
        a_drug=380,
        d_drug=10,
        generic=150,
        learn_low=["治疗持续性", "安全性", "经济性"],
        learn_high=["起效速度", "疗效", "便捷性"],
        event_no=["学科发展"],
        event_low=["治疗方案"],
        event_high=["疾病领域", "MDT外科交流", "科研相关"],
        decision_weight=0.9
    ),
    "钱医生": DoctorKnowledge(
        a_drug=380,
        d_drug=10,
        generic=150,
        learn_low=["治疗持续性", "经济性"],
        learn_high=["起效速度", "疗效", "安全性", "便捷性"],
        event_no=["学科发展", "疾病领域", "MDT交流"],
        event_low=["治疗方案"],
        event_high=["科研相关"],
        decision_weight=0.1
    ),
    # Add other doctors similarly...
}