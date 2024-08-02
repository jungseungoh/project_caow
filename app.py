# 라이브러리 불러오기 
import pandas as pd
import streamlit as st
import datetime
from streamlit_option_menu import option_menu

## 경로
IMAGE = './streamlit/image'

# 데이터 로드
data = pd.read_csv('./streamlit/sample.csv', encoding='UTF8')
data['개월령'] = data['개월령'].apply(lambda x: str(x)+' 개월')
data['육량등급'] = data['육량등급'].apply(lambda x: str(x)+' 등급')
data['BCS'] = data['BCS'].apply(lambda x: str(x)+' 등급')

# 성장 및 사육 단계에 따른 목표 체중
def feed_a(weight, month, kind): # weight:무게, month:개월, kind:품종(비육우, 번식우)
    mon = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
    wgh_1 = [50, 70, 95, 120, 145, 170, 195, 220, 245, 270, 295, 320, 345, 370, 400, 430, 460, 495, 530, 565, 600, 630, 655, 680, 700, 720, 735, 750]
    wgh_2 = [50, 70, 80, 90, 100, 120, 145, 170, 190, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 410, 430, 450, 465, 480, 500]

    if kind == '비육우':
        for i, j in zip(mon, wgh_1):
            if month <= i:
                if weight < j:
                    print(f'현재 체중이 목표체중보다 {j - weight}kg 낮습니다. \n급이량을 조금 늘려야합니다!')
                elif weight == j:
                    print(f'목표체중 {j}kg을 달성했습니다. \n')
                else:
                    print(f'현재 체중이 목표체중보다 {weight - j}kg 높습니다. \n급이량을 조금 줄여야합니다!')
                break     
    else:
        for i, j in zip(mon, wgh_2):
            if month <= i:
                if weight < j:
                    print('현재 체중이 목표체중보다 낮습니다. \n급이량을 조금 늘려야합니다!')
                elif weight == j:
                    print('목표체중을 달성했습니다. \n')
                else:
                    print('현재 체중이 목표체중보다 높습니다. \n급이량을 조금 줄여야합니다!')
                break

# 가축더위지수
def cal_thi(temperature, humidity): 
    return (1.8 * temperature + 32) - ((0.55 - 0.0055 * humidity) * (1.8 * temperature - 26.8))

# 해당 월 추출하여 계절 알아내기
def sel_season(month): 
    if 3 <= month <= 5 or 9 <= month <= 11:
        return "봄, 가을"
    elif 6 <= month <= 8:
        return "여름"
    else:
        return "겨울"

# 가축더위지수 기반 가이드
def cattle_healthcare(kind, thi, month):
    # season = sel_season(month)
    season = '여름'

    if season == "봄, 가을":
        if kind == "송아지" or kind == "비육우":
            if thi <= 71:
                return st.success("[양호]:가축사육을 위한 적정환경")
            elif 72 <= thi <= 77:
                return st.info( "[주의]:정상적인 활동, 온도 상승 경계")
            elif 78 <= thi <= 88:
                return st.warning("[경고]:사료섭취량 14%, 증체량 ~64% 감소")
            else:
                return st.error("[위험]:사료섭취량 30%, 증체량 45~75% 감소, 심박수 증가")
            
    elif season == "여름":
        if kind == "송아지":
            # thi = cal_thi(temperature, humidity)
            if thi <= 74:
                return st.success("[양호]:가축사육을 위한 적정환경")
            elif 75 <= thi <= 81:
                return st.info("[주의]:급여 5% 상향, 선풍기 작동(낮)")
            elif 82 <= thi <= 90:
                return st.warning("[경고]:심박수 증가, 직장온도 증가, 혈중 코티졸 증가, 스트레스 가중시 폐사 위험, 급여 8% 상향, 더운시간 피해 급여시간 새벽과 저녁 추천")
            else:
                return st.error("[위험]:물 부족, 심박수 증가, 직장온도 증가, 폐사율 증가, 급여 11% 상향")

        elif kind == "비육우":
            # thi = cal_thi(temperature, humidity)
            if thi <= 75:
                return st.success("[양호]:가축사육을 위한 적정환경")
            elif 76 <= thi <= 81:
                return st.info("[주의]:심박수 증가, 직장온도 증가, 혈중 glucose 증가, 급여 5% 상향")
            elif 82 <= thi <= 84:
                return st.warning("[경고]:심박수 증가, 직장온도 증가, 음수 요구량 증가, 폐사 위험, 급여 8% 상향")
            else:
                return st.error("[위험]:물 부족, 심박수 증가, 직장온도 증가, 폐사율 증가, 급여 11% 상향")

    elif season == "겨울":
        if kind == "송아지":
            if -4.2 <= temperature <= 0.7:
                return st.success("[양호]:가축사육을 위한 적정환경")
            elif -6.8 <= temperature <= -4.3:
                return st.info("[주의]:심박수 증가, 직장온도 증가, 반추 행위 감소, 바람 차단, 온수 공급")
            elif -11.1 <= temperature <= -6.9:
                return st.warning("[경고]:심박수 증가, 직장온도 증가, 사료섭취량 감소, 반추 시간 감소, 스트레스 가중시 폐사 위험, 급여 8% 상향, 마른 깔짚 제공")
            else:
                return st.error("[위험]:심박수, 직장온도 증가, 코티졸 증가, 폐사율 증가, 급여 11% 상향")
    
        elif kind == "비육우":
            if -2.4 <= temperature <= 0.7:
                return st.success("[양호]:가축사육을 위한 적정환경")
            elif -5.5 <= temperature <= -2.5:
                return st.info("[주의]:심박수 증가, 직장온도 증가, 혈중 glucose 증가, 급여 5% 상향, 온수 공급")
            elif -12.4 <= temperature <= -5.6:
                return st.warning("[경고]:심박수 증가, 직장온도 증가, 사료섭취량 감소, 반추 행위 감소, 스트레스 가중시 폐사 위험, 급여 8% 상향, 바닥상태 관리")
            else:
                return st.error("[위험]:물 부족, 심박수 증가, 직장온도 증가, 폐사율 증가")
            
# 개체 현황 시각화
def cow_management(cow_image, eartag, sensor, wgt, cow_year, cow_month, cow_day):
    now_date = datetime.datetime.today()
    months = (now_date.year - cow_year) * 12 +(now_date.month - cow_month)
    
    col2100, col2101 = st.columns([.4,.6])
    with col2100:
        path = f"{IMAGE}/{cow_image}.jpg"
        # cow_image = Image.open(path)
        # width, height = cow_image.size
        # cow_image = cow_image.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
        st.image(path)
        
    with col2101:
        col210, col211, col212, col213 = st.columns(4)
        with col210:
            st.info('이표번호')
        with col211:
            input_eartag = st.code(eartag)
        with col212:
            st.info('등록일')
        with col213:
            cow_birth = st.code(f'{cow_year}-{cow_month}-{cow_day}')

        col220, col221, col222, col223 = st.columns(4)
        with col210:
            st.info('센서번호')
        with col211:
            cow_sensor = st.code(sensor)
        with col212:
            st.info('개월령')
        with col213:
            cow_age = st.code(f'{months}')

        col230, col231, col232, col233 = st.columns(4)
        with col210:
            st.info('체중')
        with col211:
            cow_wgt = st.code(wgt)
        with col212:
            st.info('성장단계')
        with col213:
            # cow_select = st.selectbox(sensor, label_visibility='collapsed', options = ['송아지','육성우','비육우','번식우'])
            st.code('육성우')



# -------------------- ▼ 스트림릿 레이아웃 구성 ▼ --------------------

st.set_page_config(layout="wide")

# 사이드 바
with st.sidebar:
    choice = option_menu("메뉴", ["홈", "개체관리", "스트레스관리", "출하관리"],
                         icons=['house', 'kanban', 'bi bi-robot', 'calendar2-check'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "darkgreen", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"}}
    )

# 홈 화면
def main_page():
    # st.title('🏠홈')
    # 제목 넣기
    st.markdown("<h1 style='text-align: center; color: black;'>🐂 A등급 한우 육성 가이드 🐂</h1>", unsafe_allow_html=True)
    
    # 시간 정보 가져오기 
    now_date = datetime.datetime.today().strftime("%Y-%m-%d")
    
    # -------------------------------------------------------------------------------------
    
    st.markdown("#### [당진시 날씨]")
     
    col110, col111, col112, col113, col114, col115 = st.columns([0.1, 0.2, 0.1, 0.2 , 0.1, 0.2])
    with col110:
        st.info('일자')
    with col111:
        input_date = st.code(f'{now_date}')
        year, month = datetime.datetime.today().year, datetime.datetime.today().month
    with col112:
        st.info('현재 기온')
    with col113:
        input_weather = st.code('30.5°C')
        #st.metric(label='collapsed', value='30.5°C', delta='2.5')
    with col114:
        st.info('축사명')
    with col115:
        st.code('타이니팜')

    ## -------------------------------------------------------------------------------------
    
    col120, col121, col122, col123, col124, col125 = st.columns([0.1, 0.2, 0.1, 0.2, 0.1, 0.2])
    with col120:
        st.info('축사 온도')
    with col121:
        gajuk_temp = st.number_input('temp', label_visibility='collapsed', step = 0.1)
    with col122:
        st.info('축사 습도')
    with col123:
        gajuk_hum = st.number_input('hum', label_visibility='collapsed', step = 1)
    with col124:
        st.info('가축더위지수(THI)')
    with col125:
        thi = cal_thi(gajuk_temp, gajuk_hum)
        gajuk_thi = st.code(f'{thi:.2f}')

    # -------------------------------------------------------------------------------------

    col130, col131 = st.columns([0.2, 0.8])
    with col130:
        st.info('송아지 가이드')
    with col131:
        cattle_healthcare('송아지', thi, month)
    
    col140, col141 = st.columns([0.2, 0.8])
    with col140:
        st.info('비육우 가이드')
    with col141:
        cattle_healthcare('비육우', thi, month)

    st.write('')
    st.write('')
    st.write('')
    
   ## -------------------------------------------------------------------------------------

    col140, col141= st.columns([0.1, 0.1])
    with col140:
        st.markdown("#### [상태 알림]")
        st.code('3번 섹터 11번 소가 발정행위를 보입니다.')
        st.code('40번 섹터 159번 소가 야위었습니다.')
        st.code('26번 섹터 106번 소가 활동량이 전날대비 9.8% 증가하였습니다.')
    with col141:
        st.markdown("#### [오늘의 할일]")
        check = st.checkbox('1번 섹터에 있는 3번 소 상태 확인하기')
        check = st.checkbox('76번 소 육량등급 초음파 예정')
        check = st.checkbox('34번 섹터 사양관리')
        check = st.checkbox('46 ~ 50번 섹터 송아지 예방접종')
        check = st.checkbox('9번 섹터 28번 번식우 출산 예정')

    st.write('')
    st.write('')
    st.write('')
    
   ##-------------------------------------------------------------------------------------

    col150, col151= st.columns([0.1, 0.1])
    with col150:
        st.markdown("#### [축산 뉴스]")
        st.image(f"{IMAGE}/image1.png")
        st.image(f"{IMAGE}/image2.png")
        st.image(f"{IMAGE}/image3.png")
    with col151:
        st.markdown("#### [위험관리]")
        st.image(f"{IMAGE}/image6.png")
    
# 개체 현황 화면
def page2():
    st.markdown("<h1 style='text-align: center; color: black;'>🐮개체 관리🐮</h1>", unsafe_allow_html=True)
    
    col200, col201, col202, col203 = st.columns([0.2, 0.2, 0.2, .4])
    with col200:
        dong_option = st.selectbox('동',
                                   options = ['A동', 'B동', 'C동', 'D동', 'E동'])
    with col201:
        sector_option = st.selectbox('섹터',
                                     options = ['Sector1', 'Sector2', 'Sector3', 'Sector4', 'Sector5','Sector6'])
    with col202:
        select_id = st.selectbox('이표번호',
                                 options = ['Sector1', '9990 3040 1', '9990 3040 2', '9990 3040 3', '9990 3040 4'])
    with col203:
        st.write('')
        st.write('')

   ## -------------------------------------------------------------------------------------    

    ids = {x:i for i, x in enumerate(['Sector1', '9990 3040 1', '9990 3040 2', '9990 3040 3', '9990 3040 4'])}
    c_id = ids[select_id]
    cow_img = ['all', '1', '2', '3', '4'][c_id]
    if select_id == 'Sector1':
        st.image(f"{IMAGE}/cow_{cow_img}.jpg")
    else:
        sensors = [0, 'D041194', 'D041195', 'D041196', 'D041197', ]
        weights = [0, '600kg(A)', '430kg(C)', '520kg(B)', '560kg(B)']
        years = [2021]*5
        months = [3,1,3,3,2]
        days = [4,4,10,6,28]
        cow_management(f'cow_{cow_img}', select_id, sensors[c_id], weights[c_id], years[c_id], months[c_id], days[c_id])
            
# 급이관리 화면
def page3():
    st.markdown("<h1 style='text-align: center; color: black;'>🌱스트레스 관리🌱</h1>", unsafe_allow_html=True)
    st.write('')
    st.write('')
    
    col301, col302, col303, col304= st.columns(4)
    with col301:
        st1 = '<p style="font-family:Noto Serif KR; color:#22741C; font-size: 20px; font-weight: bold;">양호</p>'
        st.markdown(st1, unsafe_allow_html=True)
        st.metric(label = '', value = '91마리', delta = '전날 대비 4마리', label_visibility='collapsed')
    with col302:
        st1 = '<p style="font-family:Noto Serif KR; color:#FFE400; font-size: 20px; font-weight: bold;">주의</p>'
        st.markdown(st1, unsafe_allow_html=True)
        st.metric(label = '', value = '20마리', delta = '-전날 대비 2마리', label_visibility='collapsed')
    with col303:
        st1 = '<p style="font-family:Noto Serif KR; color:Orange; font-size: 20px; font-weight: bold;">경고</p>'
        st.markdown(st1, unsafe_allow_html=True)
        st.metric(label = '', value = '8마리', delta = '전날 대비 1마리', label_visibility='collapsed')
    with col304:
        st1 = '<p style="font-family:Noto Serif KR; color:Red; font-size: 20px; font-weight: bold;">위험</p>'
        st.markdown(st1, unsafe_allow_html=True)
        st.metric(label = '', value = '3마리', delta = '-전날 대비 3마리', label_visibility='collapsed')
    st.write('')
    
   ## -------------------------------------------------------------------------------------    
    
    st.image(f"{IMAGE}/care1.png")
    
# 출하일정 화면
def page4():
    st.markdown("<h1 style='text-align: center; color: black;'>📆출하 관리📆</h1>", unsafe_allow_html=True)
    st.write('')
    st.write('')
    
    st.markdown('### AI 예측 등급')

    st.dataframe(
        data,
        width = 1200,
        # column_config={
        #     "예상확률": st.column_config.ProgressColumn(
        #         "확률(%)",help="BCS",
        #         format="%f",
        #         min_value=0, max_value=100,
        #     )
        # }, 
    )
    
    st.write('')
    st.write('')
    
   ## -------------------------------------------------------------------------------------    
    
    col4001, col4002 = st.columns([.3,.7])
    with col4001:
        st.image(f"{IMAGE}/cow/c1_r.jpg")
    with col4002: 
        st.image(f"{IMAGE}/cow/c2_r.png", width=580)
        
# 사이드바에서 선택한 메뉴로 화면 바꾸기
page_names = {'홈': main_page, '개체관리':page2, '스트레스관리':page3, '출하관리':page4}
page_names[choice]()
