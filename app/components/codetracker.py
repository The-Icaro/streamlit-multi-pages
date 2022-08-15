import streamlit as st
import re

from app.service.delivery_api import get_all_deliveryman, get_all_buyers
from app.helper.selectbox_builder import data_selectbox_builder
from app.service.cep_api import get_address_by_zipcode
from app.helper.code_generator import code_generator

buyer_code = code_generator()


def codetracker():
    def handleVerifyCodeCheck(correct_code, input_code):
        if correct_code == input_code:
            st.success("Sua Entrega foi Realizada com Sucesso")
        else:
            st.warning("Entrega Cancelada")

    st.header("Code Tracker")

    st.markdown(
        """
                    <style>
                      @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@300&family=Roboto+Mono:wght@300&display=swap');
                      * {
                          font-family: 'Nunito', sans-serif;
                      }
                      #MainMenu {visibility: hidden;}
                      .css-k0sv6k {
                            position: fixed;
                            top: 0px;
                            left: 0px;
                            right: 0px;
                            height: 2.875rem;
                            background: rgb(255, 255, 255) none repeat scroll 0% 0%;
                            outline: currentcolor none medium;
                            z-index: 1000020;
                            display: none;
                      }
                      .css-rytr0c {
                            vertical-align: middle;
                            overflow: hidden;
                            color: rgb(151, 166, 195);
                            fill: currentcolor;
                            display: inline-flex;
                            -moz-box-align: center;
                            align-items: center;
                            font-size: 1.25rem;
                            width: 1.25rem;
                            height: 1.25rem;
                            display: none;
                        }
                      .css-fg4pbf {
                          position: absolute;
                          background: #ffe8e8;
                          color: rgb(49, 51, 63);
                          inset: 0px;
                          overflow: hidden;
                      }
                      .css-1ht1j8u {
                          overflow-wrap: normal;
                          text-overflow: ellipsis;
                          width: 100%;
                          overflow: hidden;
                          white-space: nowrap;
                          font-family: 'Nunito', sans-serif;
                          line-height: normal;
                      }
                      .css-12oz5g7 {
                          flex: 1 1 0%;
                          width: 100%;
                          padding: 6rem 1rem 10rem;
                          max-width: 80rem;
                      }
                      .css-10trblm {
                          position: relative;
                          flex: 1 1 0%;
                          margin-left: calc(3rem);
                          text-align: center;
                      }
                      .css-keje6w {
                        width: calc(50% - 1rem);
                        flex: 1 1 calc(50% - 1rem);
                        background-color: #FFF;
                        border-radius: 15px;
                        padding: 15px;
                      }
                      .css-qrbaxs {
                        font-size: 20px;
                        color: rgb(49, 51, 63);
                        margin-bottom: 7px;
                        height: auto;
                        min-height: 1.5rem;
                        vertical-align: middle;
                        display: flex;
                        flex-direction: row;
                        -moz-box-align: center;
                        align-items: center;
                      }
                      .css-1r6slb0 {
                        width: calc(33.3333% - 1rem);
                        flex: 1 1 calc(33.3333% - 1rem);
                        background-color: #FFF;
                        border-radius: 15px;
                        padding: 15px;
                      }
                      .css-jhf39w {
                        font-size: 20px;
                        color: rgb(49, 51, 63);
                        margin-bottom: 7px;
                        height: auto;
                        min-height: 1.5rem;
                        vertical-align: middle;
                        display: flex;
                        flex-direction: row;
                        -moz-box-align: center;
                        align-items: center;
                      }
                      .css-1cpxqw2 {
                        -moz-box-align: center;
                        -moz-box-pack: center;
                        font-weight: 400;
                        padding: 0.25rem 0.75rem;
                        border-radius: 0.25rem;
                        margin: 0px;
                        line-height: 1.6;
                        color: inherit;
                        user-select: none;
                        background-color: rgb(255, 255, 255);
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        width: 100%;
                      }
                      .css-1siy2j7 {
                          background-color: #FFF;
                          background-attachment: fixed;
                          flex-shrink: 0;
                          height: calc(-2px + 100vh);
                          top: 2px;
                          overflow: auto;
                          position: relative;
                          transition: margin-left 300ms ease 0s, box-shadow 300ms ease 0s;
                          width: 21rem;
                          z-index: 1000021;
                          margin-left: 0px;
                          border-radius: 0px 15px;
                      }
                      .css-1qrvfrg {
                          display: inline-flex;
                          -moz-box-align: center;
                          align-items: center;
                          -moz-box-pack: center;
                          justify-content: center;
                          font-weight: 400;
                          padding: 0.25rem 0.75rem;
                          margin: 0px;
                          line-height: 1.6;
                          color: inherit;
                          user-select: none;
                          border: 1px solid #FFF;
                          width: 100%;
                          background-color: #FFF;
                      }
                      .css-1qrvfrg:hover {
                          border-color: #79AFFF;
                          color: #79AFFF;
                      }
                      .css-1qrvfrg:active {
                          color: #FFF;
                          border-color: #79AFFF;
                          background-color: #79AFFF;
                      }
                      .css-1qrvfrg:focus {
                          box-shadow: #79AFFF 0px 0px 0px 0.2rem;
                          outline: #79AFFF none medium;
                      }
                      .css-1qrvfrg:focus:not(:active) {
                          border-color: #79AFFF;
                          color: #79AFFF;
                      }
                    </style>
                """,
        unsafe_allow_html=True,
    )

    buyers = get_all_buyers()
    delivery_mens = get_all_deliveryman()

    select_box_buyers_options = data_selectbox_builder(buyers)
    select_box_delivery_mens_options = data_selectbox_builder(delivery_mens)

    c1, c2 = st.columns((3, 3))

    with c1:
        st.selectbox("Selecione o Entregador", tuple(select_box_delivery_mens_options))

    with c2:
        buyer = st.selectbox("Selecione o Comprador", tuple(select_box_buyers_options))

    st.subheader("Dados da Rota")

    buyer_id = re.findall(r"\d+", buyer)[0]
    buyerData = next(
        (buyer for buyer in buyers if buyer.get("id") == int(buyer_id)), None
    )

    zip_code = buyerData.get("cep")
    address_data = get_address_by_zipcode(zip_code)

    col1, col2, col3 = st.columns(3)
    col1.text(f"Cep : {zip_code}")
    col2.text(f"Estado : {address_data.get('uf')}")
    col3.text(f"Cidade : {address_data.get('localidade')}")

    col4, col5, col6 = st.columns(3)
    col4.text(f"Bairro : {address_data.get('bairro')}")
    col5.text(f"Rua : {address_data.get('logradouro')}")
    col6.text(f"Número : {buyerData.get('addressNumber')}")

    column1, column2 = st.columns((3, 3))

    with column1:
        st.text_input(
            "Favor informar Código de Segurança ao Entregador:",
            disabled=True,
            placeholder=buyer_code,
        )

    with column2:
        received_code = st.text_input(
            "Insira o Código de Entrega informado pelo Comprador:"
        )

    _, cl2, _ = st.columns((1, 4, 1))

    with cl2:
        if st.button("Verificar Código de Segurança"):
            handleVerifyCodeCheck(buyer_code, received_code)
