def extract_galileo_ionospheric_corr(filepath):
    """
    RINEX Navigation 파일에서 Galileo 전리층 보정 계수 a0, a1, a2 추출
    :param filepath: .rnx 파일 경로
    :return: (a0, a1, a2) 또는 None
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "GALILEO IONOSPHERIC CORR" in line:
                try:
                    parts = line.strip().split()
                    a0, a1, a2 = map(float, parts[:3])
                    return a0, a1, a2
                except Exception as e:
                    print("파싱 오류:", e)
                    return None
    print("GALILEO IONOSPHERIC CORR 항목을 찾을 수 없습니다.")
    return None

# ✅ 사용 예시
if __name__ == "__main__":
    filepath = "YONS00KOR_R_20250820000_01D_30S_MN.rnx"  # 당신의 RINEX 파일 경로
    result = extract_galileo_ionospheric_corr(filepath)
    
    if result:
        a0, a1, a2 = result
        print(f"📡 추출된 계수:\na0 = {a0}\na1 = {a1}\na2 = {a2}")
    else:
        print("❌ 계수 추출 실패")
