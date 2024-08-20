import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# 나눔 고딕 폰트 경로 찾기
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 리눅스 경로 예시
# Windows에서 경로는 다를 수 있습니다. 예: 'C:\\Windows\\Fonts\\NanumGothic.ttf'

# 폰트 패밀리 등록
font_manager.fontManager.addfont(font_path)
rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()

# 폰트가 적용된 그래프 예시
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, '안녕하세요', fontsize=20, ha='center')
plt.show()
