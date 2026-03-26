import streamlit as st
import pandas as pd
import os

# --- アプリの裏側の仕組み（状態の記憶） ---
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'category' not in st.session_state:
    st.session_state.category = ""
if 'symptom' not in st.session_state:
    st.session_state.symptom = ""

# ページを移動する機能
def change_page(page_num):
    st.session_state.page = page_num

def select_category(cat_name):
    st.session_state.category = cat_name
    st.session_state.page = 3

def select_symptom(sym_name):
    st.session_state.symptom = sym_name
    st.session_state.page = 4

# 安全確認の判定ルール
def check_safety():
    if st.session_state.preg == "はい" or st.session_state.allergy == "はい":
        st.session_state.page = 6
    else:
        st.session_state.page = 5

# ▼▼▼ 修正箇所①：インターネット上でも動くように「相対パス」に変更 ▼▼▼
@st.cache_data
def load_data():
    return pd.read_excel("medicines.xlsx")
# ▲▲▲ ここまで ▲▲▲

# --- 親しみやすいデザインと文字サイズの修正 ---
def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Zen Maru Gothic', sans-serif !important;
            color: #5D4037 !important;
        }

        h1 {
            font-size: 1.6rem !important;
            color: #E67E22 !important;
            line-height: 1.4 !important;
        }
        h2, h3 {
            color: #E67E22 !important;
        }

        div[data-testid="stButton"] > button {
            border-radius: 30px !important;
            border: 2px solid #FAE5D3 !important;
            background-color: #FFFAFA !important;
            color: #5D4037 !important;
            box-shadow: 0 4px 6px rgba(230, 126, 34, 0.08) !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
        }

        div[data-testid="stButton"] > button:hover {
            border-color: #F39C12 !important;
            color: #D35400 !important; 
            box-shadow: 0 6px 8px rgba(230, 126, 34, 0.15) !important;
            transform: translateY(-2px) !important;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #F39C12 !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700 !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #D35400 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 2%; 
        }
        div[data-testid="stColumn"], div[data-testid="column"] {
            width: 49% !important;
            flex: 1 1 49% !important;
            min-width: 49% !important;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_css()


# --- ここから画面の表示内容 ---

# 📱 画面1：スタート画面
if st.session_state.page == 1:
    st.title("💊 お薬ぴったり検索")
    st.write("今のあなたに合った市販薬をご案内します。")
    st.info("※最終的なご購入の判断は、店舗の薬剤師・登録販売者にご相談ください。")
    st.button("検索をはじめる", on_click=change_page, args=(2,), type="primary", use_container_width=True)

# 📱 画面2：大きな症状の選択
elif st.session_state.page == 2:
    st.title("気になる症状は？")
    st.write("当てはまるものを1つ選んでください。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🤧 風邪（かぜ）", on_click=select_category, args=("風邪",), use_container_width=True)
        st.button("🤢 胃腸の不調",   on_click=select_category, args=("胃腸の不調",), use_container_width=True)
        st.button("👃 鼻のトラブル", on_click=select_category, args=("鼻のトラブル",), use_container_width=True)
        st.button("💥 肩こり・腰痛", on_click=select_category, args=("肩こり・腰痛",), use_container_width=True)
    with col2:
        st.button("🤕 痛み・熱",     on_click=select_category, args=("痛み・熱",), use_container_width=True)
        st.button("👁️ 目のトラブル", on_click=select_category, args=("目のトラブル",), use_container_width=True)
        st.button("🩹 皮膚のトラブル",on_click=select_category, args=("皮膚のトラブル",), use_container_width=True)
        st.button("🔋 その他(疲れ等)",on_click=select_category, args=("その他",), use_container_width=True)

    st.divider()
    st.button("◀ 最初の画面に戻る", on_click=change_page, args=(1,))


# 📱 画面3：詳細な症状の選択
elif st.session_state.page == 3:
    st.title(f"【{st.session_state.category}】")
    st.write("最もつらい症状はどれですか？")

    if st.session_state.category == "風邪":
        st.button("のどの痛み", on_click=select_symptom, args=("のどの痛み",), use_container_width=True)
        st.button("熱・さむけ", on_click=select_symptom, args=("熱・さむけ",), use_container_width=True)
        st.button("鼻水・鼻づまり", on_click=select_symptom, args=("鼻水・鼻づまり",), use_container_width=True)
        st.button("せき・たん", on_click=select_symptom, args=("せき・たん",), use_container_width=True)

    elif st.session_state.category == "痛み・熱":
        st.button("頭痛", on_click=select_symptom, args=("頭痛",), use_container_width=True)
        st.button("生理痛", on_click=select_symptom, args=("生理痛",), use_container_width=True)
        st.button("関節痛・歯痛", on_click=select_symptom, args=("関節痛・歯痛",), use_container_width=True)
        st.button("急な発熱", on_click=select_symptom, args=("急な発熱",), use_container_width=True)

    elif st.session_state.category == "胃腸の不調":
        st.button("胃痛・胃酸過多", on_click=select_symptom, args=("胃痛",), use_container_width=True)
        st.button("胃もたれ・食べすぎ", on_click=select_symptom, args=("胃もたれ",), use_container_width=True)
        st.button("下痢", on_click=select_symptom, args=("下痢",), use_container_width=True)
        st.button("便秘", on_click=select_symptom, args=("便秘",), use_container_width=True)

    elif st.session_state.category == "鼻のトラブル":
        st.button("アレルギー（花粉・ハウスダスト）", on_click=select_symptom, args=("アレルギー性鼻炎",), use_container_width=True)
        st.button("ドロっとした鼻水（蓄膿症など）", on_click=select_symptom, args=("副鼻腔炎",), use_container_width=True)

    elif st.session_state.category == "肩こり・腰痛":
        st.write("※痛みの種類や、ご希望のお薬のタイプに合わせてお選びください。")
        st.button("慢性的な肩こり（温めると楽になる）", on_click=select_symptom, args=("肩こり（慢性・温感）",), use_container_width=True)
        st.button("急な首・肩の痛み（寝違え・スジちがい等）", on_click=select_symptom, args=("肩こり（急性・冷感）",), use_container_width=True)
        st.button("慢性的な腰痛（温めると楽になる）", on_click=select_symptom, args=("腰痛（慢性・温感）",), use_container_width=True)
        st.button("急な腰痛（ぎっくり腰など）", on_click=select_symptom, args=("腰痛（急性・冷感）",), use_container_width=True)
        st.button("関節痛・筋肉痛（サッと塗れる液剤・ジェルなど）", on_click=select_symptom, args=("関節痛・筋肉痛（塗布剤）",), use_container_width=True)

    elif st.session_state.category == "目のトラブル":
        st.button("目の疲れ・かすみ", on_click=select_symptom, args=("目の疲れ",), use_container_width=True)
        st.button("充血", on_click=select_symptom, args=("充血",), use_container_width=True)
        st.button("目のかゆみ（花粉など）", on_click=select_symptom, args=("かゆみ",), use_container_width=True)
        st.button("ドライアイ（乾燥）", on_click=select_symptom, args=("ドライアイ",), use_container_width=True)
        st.button("ものもらい・結膜炎", on_click=select_symptom, args=("ものもらい・結膜炎",), use_container_width=True)

    elif st.session_state.category == "皮膚のトラブル":
        st.button("かゆみ・虫刺され", on_click=select_symptom, args=("かゆみ・虫刺され",), use_container_width=True)
        st.button("乾燥肌・乾燥によるかゆみ", on_click=select_symptom, args=("乾燥肌",), use_container_width=True)
        st.button("しっしん・かぶれ", on_click=select_symptom, args=("しっしん・かぶれ",), use_container_width=True)
        st.button("傷・やけど", on_click=select_symptom, args=("傷・やけど",), use_container_width=True)
        st.button("ニキビ", on_click=select_symptom, args=("ニキビ",), use_container_width=True)
        st.button("水虫", on_click=select_symptom, args=("水虫",), use_container_width=True)

    elif st.session_state.category == "その他":
        st.button("疲れ・だるさ（栄養補給）", on_click=select_symptom, args=("疲れ",), use_container_width=True)
        st.button("乗り物酔い", on_click=select_symptom, args=("乗り物酔い",), use_container_width=True)
        st.button("睡眠の悩み（一時的な不眠）", on_click=select_symptom, args=("睡眠改善",), use_container_width=True)
        st.button("更年期・生理不順など（女性の悩み）", on_click=select_symptom, args=("女性の悩み",), use_container_width=True)
        st.button("頻尿・夜間尿・残尿感（尿の悩み）", on_click=select_symptom, args=("尿の悩み",), use_container_width=True)

    st.divider()
    st.button("◀ 症状を選び直す", on_click=change_page, args=(2,))


# 📱 画面4：安全確認
elif st.session_state.page == 4:
    st.title("✅ 安全確認")
    st.write("安全にお薬をご案内するため、該当するものをお選びください。")
    
    st.radio("👤 お薬を使う方の年齢は？", ["15歳以上（大人）", "7歳〜14歳", "7歳未満"], key="age")
    st.radio("🤰 妊娠中・授乳中ですか？", ["いいえ", "はい"], key="preg")
    st.radio("🏥 お薬でアレルギーが出たことや、治療中の病気はありますか？", ["いいえ", "はい"], key="allergy")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.button("◀ 戻る", on_click=change_page, args=(3,), use_container_width=True)
    with col2:
        st.button("結果を見る", on_click=check_safety, type="primary", use_container_width=True)


# 📱 画面5：結果表示
elif st.session_state.page == 5:
    st.title("💊 おすすめのお薬")
    
    st.write(f"**症状：** {st.session_state.category} ＞ {st.session_state.symptom}")
    st.write(f"**対象：** {st.session_state.age}")
    st.divider()

    try:
        df = load_data()
        filtered_df = df[(df["カテゴリ"] == st.session_state.category) & (df["症状"] == st.session_state.symptom)]
        
        age_column = st.session_state.age
        filtered_df = filtered_df[filtered_df[age_column] == "〇"]

        filtered_df = filtered_df[filtered_df["商品名"] != "-"]

        if filtered_df.empty:
            st.warning("申し訳ありません。ご指定の条件にぴったり合うお薬がリストに見つかりませんでした。")
            st.write("店舗スタッフが最適なものをお探ししますので、お気軽にお声がけください。")
        else:
            st.success("以下の商品がおすすめです！店頭でお探しください。")
            
            for index, row in filtered_df.iterrows():
                st.markdown(f"### 🏷️ {row['商品名']}")
                
                # ▼▼▼ 修正箇所②：インターネット上でも動くように「相対パス」に変更 ▼▼▼
                if '画像' in df.columns and pd.notna(row['画像']):
                    img_path = os.path.join("images", str(row['画像']))
                    if os.path.exists(img_path):
                        st.image(img_path, width=250)
                # ▲▲▲ ここまで ▲▲▲
                
                st.info(f"✨ **特徴:** {row['特徴・おすすめポイント']}")
                st.write("") 

    except Exception as e:
        st.error(f"データの読み込みに失敗しました。エラー詳細: {e}")

    st.divider()
    st.button("最初からやり直す", on_click=change_page, args=(1,), type="primary", use_container_width=True)


# 📱 画面6：薬剤師・登録販売者へ相談（ストップ画面）
elif st.session_state.page == 6:
    st.title("👨‍⚕️ 店舗スタッフにご相談ください")
    
    st.markdown("<div style='text-align: center; font-size: 80px; margin: 20px 0;'>🙇‍♂️</div>", unsafe_allow_html=True)
    
    st.write("妊娠中・授乳中の方、またはアレルギーや治療中の病気がある方は、お薬の成分によって思わぬ影響が出る可能性があります。")
    st.write("**お手数ですが、直接店舗の薬剤師または登録販売者にご相談ください。**")
    
    st.divider()
    st.button("最初からやり直す", on_click=change_page, args=(1,), type="primary", use_container_width=True)