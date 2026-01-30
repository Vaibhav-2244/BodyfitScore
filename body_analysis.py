def calculate_score(m, gender):
    score = 0.0

    # -------- Upper body contribution --------
    chest_ratio = m["chest"] / m["waist"]

    if chest_ratio >= 1.4:
        score += 3.0
    elif chest_ratio >= 1.3:
        score += 2.5
    elif chest_ratio >= 1.2:
        score += 2.0
    elif chest_ratio >= 1.1:
        score += 1.5
    else:
        score += 1.0

    # -------- Arms (male emphasis) --------
    if gender == "male":
        arm_ratio = m["arms"] / m["chest"]
        if arm_ratio >= 0.7:
            score += 1.5
        elif arm_ratio >= 0.6:
            score += 1.2
        elif arm_ratio >= 0.5:
            score += 0.8
        else:
            score += 0.5

    # -------- Core / waist balance --------
    if m["waist"] < m["chest"] * 0.85:
        score += 1.5
    elif m["waist"] < m["chest"] * 0.95:
        score += 1.2
    else:
        score += 0.8

    # -------- Lower body (thighs & hips) --------
    thigh_ratio = m["thighs"] / m["hips"]

    if thigh_ratio >= 1.0:
        score += 2.0
    elif thigh_ratio >= 0.9:
        score += 1.6
    elif thigh_ratio >= 0.85:
        score += 1.2
    else:
        score += 0.8

    # -------- Female hip structure bonus --------
    if gender == "female":
        hip_ratio = m["hips"] / m["waist"]
        if hip_ratio >= 1.35:
            score += 1.5
        elif hip_ratio >= 1.25:
            score += 1.2
        else:
            score += 0.8

    # Clamp to 10
    return round(min(10.0, max(3.5, score)), 1)


def generate_message(m, gender, score):
    msg = []

    chest_ratio = m["chest"] / m["waist"]
    thigh_ratio = m["thighs"] / m["hips"]

    # =======================
    # MALE BODY INTERPRETATION
    # =======================
    if gender == "male":

        # ---- Chest ----
        if chest_ratio >= 1.4:
            msg.append(
                "Your chest is significantly wider than your waist, creating a strong and athletic upper-body frame."
            )
        elif chest_ratio >= 1.3:
            msg.append(
                "Your chest shows good width relative to your waist, indicating solid upper-body development."
            )
        elif chest_ratio >= 1.2:
            msg.append(
                "Your chest is moderately wider than your waist, suggesting a developing upper-body structure."
            )
        else:
            msg.append(
                "Your chest appears relatively narrow compared to your waist, indicating that upper-body strength can be improved."
            )

        # ---- Arms ----
        arm_ratio = m["arms"] / m["chest"]
        if arm_ratio >= 0.7:
            msg.append(
                "Your arms appear well-developed and proportionate to your chest, contributing to a balanced upper body."
            )
        elif arm_ratio >= 0.6:
            msg.append(
                "Your arms show moderate development but can gain more definition with focused training."
            )
        else:
            msg.append(
                "Your arms appear lean relative to your chest, suggesting scope for muscle growth."
            )

        # ---- Waist ----
        if m["waist"] < m["chest"] * 0.85:
            msg.append(
                "Your waist is well-controlled, enhancing the overall shape of your torso."
            )
        else:
            msg.append(
                "Improving core strength and waist control would noticeably enhance your physique."
            )

        # ---- Thighs ----
        if thigh_ratio >= 1.0:
            msg.append(
                "Your thighs are strong and well-developed, providing a solid lower-body foundation."
            )
        elif thigh_ratio >= 0.9:
            msg.append(
                "Your thighs show decent development, though additional lower-body training could improve balance."
            )
        else:
            msg.append(
                "Your thighs appear relatively lean compared to your hips, indicating lower-body strength can be improved."
            )

    # =========================
    # FEMALE BODY INTERPRETATION
    # =========================
    else:

        hip_ratio = m["hips"] / m["waist"]

        # ---- Hips ----
        if hip_ratio >= 1.35:
            msg.append(
                "Your hips are noticeably wider than your waist, giving a naturally curvier lower-body structure."
            )
        elif hip_ratio >= 1.25:
            msg.append(
                "Your hip-to-waist ratio shows healthy and balanced lower-body proportions."
            )
        else:
            msg.append(
                "Your hips and waist appear closely aligned, creating a straighter body outline."
            )

        # ---- Thighs ----
        if thigh_ratio >= 1.0:
            msg.append(
                "Your thighs are strong and well-shaped relative to your hips."
            )
        elif thigh_ratio >= 0.9:
            msg.append(
                "Your thighs show moderate strength with potential for improved tone."
            )
        else:
            msg.append(
                "Your thighs appear lean relative to your hips, suggesting scope for muscle toning."
            )

        # ---- Chest / Upper body ----
        if chest_ratio >= 1.2:
            msg.append(
                "Your upper body is well-proportioned relative to your waist, supporting a balanced frame."
            )
        else:
            msg.append(
                "Strengthening the upper body can improve overall body balance and posture."
            )

        # ---- Waist ----
        if m["waist"] < m["hips"] * 0.8:
            msg.append(
                "Your waist is well-defined, enhancing natural body curves."
            )
        else:
            msg.append(
                "Improving core strength can help enhance waist definition."
            )

    # =======================
    # SCORE-BASED CLOSING
    # =======================
    if score >= 8.5:
        closing = (
            "Overall, your body proportions reflect disciplined training and strong structural balance."
        )
    elif score >= 7.0:
        closing = (
            "Your body shows good balance and fitness, with clear potential for further refinement."
        )
    elif score >= 5.5:
        closing = (
            "You have a solid base, and consistent effort can bring noticeable improvements."
        )
    else:
        closing = (
            "With regular activity and targeted training, visible progress is very achievable."
        )

    msg.append(closing)

    return " ".join(msg)
