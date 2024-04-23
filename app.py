#Importing Modules
import streamlit as st
import numpy as np
from PIL import Image
import numpy as np
from util import set_background, get_colour_name
import requests
import time
from io import BytesIO
from PIL import ImageColor
from streamlit_image_comparison import image_comparison

#API URL
API_URL_ENDPOINT = "https://827f-34-90-151-246.ngrok-free.app/"

#st.set_page_config(layout="wide", page_title="Image Background Remover")
set_background("./imgs/background.png")

#Function to Send and Recieve the Image to the API
def get_hair_roots_edited_img(img, inpaint_option, hair_color, automatic_hair_root_area) :
    bytes_data = img.getvalue()
    resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})
    #st.write(resp.content)
    return resp.content

#Creating Section of the Web UI with Streamlit
header = st.container()
body = st.container()

st.sidebar.markdown('''
    🧑🏻‍💻 `Proyecto de Expociencia Programacion III UBA`
    ''')

#Frontend Sidebar with Streamlit
st.sidebar.markdown("---------")
st.sidebar.title("Proyecto de Modificacion de Cabello 👱🏻‍♀️")
st.sidebar.subheader("Retoque de las Raices del Pelo Utilizando Stable Diffusion y ControlNet 💈")
#st.sidebar.image("./imgs/preview2.gif")
st.sidebar.markdown("---------")
st.markdown(
    """
    <style>
    [data-testid="stSidebar][aria-expanded="true"] > div:first-child{
        width: 350px
    }
    [data-testid="stSidebar][aria-expanded="false"] > div:first-child{
        width: 350px
        margin-left: -350px
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.subheader("Sube una Imagen:")
img_option = st.sidebar.radio("Opciones:", ["Cargar Imagen", "Tomar Fotografia"], horizontal=True)
if img_option == "Cargar Imagen" :
    img_file = st.sidebar.file_uploader("Carga la Imagen:", type=["jpg", "png", "jpeg"])
elif img_option == "Tomar Fotografia" :
    st.markdown("<hr/>", unsafe_allow_html=True)
    img_file = st.camera_input(" ")
    st.sidebar.markdown('''
    🚨 `Para Mejor Resultado, Captar la Fotografia tipo Autorretrato del Cabello de la Persona` 📸
    ''')

if img_file is not None :
    inpaint_option = st.sidebar.radio("Ediciones:", ["Retocar las Raices", "Modificar todo el Cabello"], horizontal=True)
    hair_color = ""
    if (inpaint_option == "Modificar todo el Cabello") :
        automatic_hair_root_area=""
        inpaint_option = "Touch-up whole Hair"
        column1, column2 = st.sidebar.columns([0.8, 0.2])
        hair_color = column1.text_input("Especifica un Color de Pelo:")
        hex_code_color = column2.color_picker("Escoger:")
        
        rgb_code_color = ImageColor.getcolor(hex_code_color, "RGB")
        actual_name, closest_name = get_colour_name(rgb_code_color)
        
        if (hair_color == "") :
            if (actual_name == None) :
                hair_color = (closest_name + '.')[:-1]
            elif (actual_name != None) :
                hair_color = (actual_name + '.')[:-1]
    elif (inpaint_option == "Retocar las Raices") :
        inpaint_option = "Touch-up Hair Roots"
        automatic_hair_root_area = st.sidebar.checkbox("Seleccion Automatica del Area de la Raiz del Cabello", value=True)

    image = np.array(Image.open(img_file))
    st.sidebar.image(image)

    _, col, _ = st.sidebar.columns([0.3, 0.5, 0.2])
    if col.button("Generar Imagen", type="primary") :
        with st.spinner(text="Generando Imagen..."):
            #Sending the Image to the API function
            try :

                hair_roots_touchup_img = get_hair_roots_edited_img(img_file, inpaint_option, hair_color, automatic_hair_root_area)
                pillow_img = Image.open(BytesIO(hair_roots_touchup_img)).convert('RGB')

                progress_bar = st.progress(0)
                for perc_completed in range(100) :
                    time.sleep(0.001)
                    progress_bar.progress(perc_completed+1)

                st.markdown("<hr/>", unsafe_allow_html=True)
                st.success("Imagen Generada Satisfactoriamente ✅")
                st.markdown("<hr/>", unsafe_allow_html=True)

                #_, col3, _ = st.columns([0.5,1,0.5])
                #col3.subheader("Resultados Generados ✅")

                image_comparison(
                    img1=image, img2=pillow_img,
                    label1='Original', label2='Modificada',
                )
                
                st.markdown("<hr/>", unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])
                col1.image(image, use_column_width=True, caption="Imagen Original 🖼️")
                col2.image(hair_roots_touchup_img, use_column_width=True, caption="Cabello Modificado 💇🏻‍♂️")

                st.markdown("<hr/>", unsafe_allow_html=True)
                buf = BytesIO()
                pillow_img.save(buf, format="JPEG")
                byte_im = buf.getvalue()

                _, col4, _ = st.columns([1, 1, 1])
                col4.download_button(
                    label="Descargar Imagen Generada",
                    data=byte_im,
                    file_name="hair_roots_touchup_img.jpeg",
                    mime="image/jpeg",
                    )    
            except :
                st.markdown("<hr/>", unsafe_allow_html=True)
                st.error("Hubo un Error, Intentalo Nuevamente ⚠️")
                st.markdown("<hr/>", unsafe_allow_html=True)    
            
with header :
    st.title("App para Modificar el Cabello 👩🏻‍🦰")
    st.markdown("<hr/>", unsafe_allow_html=True)

with body :
    st.subheader("Modifica Rapidamente las Raices del Pelo de una Persona en un Momento 💇🏻")
    st.write("Sube la Foto a Modificar en la Barra Lateral. Para Modificar el Cabello, se van a utilizar distintos Modelos de I.A. como Stable Diffusion, ControlNet, KMeans y Mediapipe.")
