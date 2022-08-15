import streamlit as st
import re
import pandas as pd

from app.service.delivery_api import (
    get_all_deliveries,
    find_deliveryman_by_id,
    find_buyer_by_id,
)
from app.helper.selectbox_builder import delivery_selectbox_buider


def deliverytracker():
    def handleShippedDelivery(
        latitudes: list, longitudes: list, delivery_status: str, documents: list
    ):

        if delivery_status != "DONE":
            return

        if latitudes[0] != latitudes[1] and longitudes[0] != longitudes[1]:
            st.error("Entrega em Locais Diferentes")
            return

        if latitudes[0] == latitudes[1] and longitudes[0] == longitudes[1]:

            if documents[0] != documents[1]:
                st.warning(
                    f"Produto Entregue para Pessoa com Documento Diferente, Verificar com {'{}.{}.{}-{}'.format(documents[1][:3], documents[1][3:6], documents[1][6:9], documents[1][9:])}"
                )
            else:
                st.success("Entrega Realizada Com Sucesso!")
            return

    st.header("Delivery Tracker")

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
                        .stSelectbox {
                            background-color: rgb(255, 255, 255);
                            padding: 10px;
                            border-radius: 15px;
                        }
                        .css-keje6w {
                            width: calc(50% - 1rem);
                            flex: 1 1 calc(50% - 1rem);
                            background-color: rgb(255, 255, 255);
                            padding: 20px;
                            border-radius: 15px;
                        }
                        .css-115gedg  {
                            width: calc(66.6667% - 1rem);
                            flex: 1 1 calc(66.6667% - 1rem);
                            background-color: rgb(255, 255, 255);
                            padding: 20px;
                            border-radius: 15px;
                        }
                        .css-1r6slb0 {
                            width: calc(66.6667% - 1rem);
                            flex: 1 1 calc(66.6667% - 1rem);
                            background-color: rgb(255, 255, 255);
                            padding: 20px;
                            border-radius: 15px;
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
                    </style>
                """,
        unsafe_allow_html=True,
    )

    deliveries = get_all_deliveries()

    select_box_deliveries_options = delivery_selectbox_buider(deliveries)
    delivery_selected = st.selectbox(
        "Selecione a Entrega", tuple(select_box_deliveries_options)
    )

    delivery_id = re.findall(r"\d+", delivery_selected)[0]
    deliveryData = next(
        (delivery for delivery in deliveries if delivery.get("id") == int(delivery_id)),
        None,
    )

    deliveryman = find_deliveryman_by_id(deliveryData.get("idDeliveryman"))
    buyer = find_buyer_by_id(deliveryData.get("idBuyer"))

    lats = [deliveryData.get("deliverymanLat"), buyer.get("addressLat")]
    longs = [deliveryData.get("deliverymanLong"), buyer.get("addressLong")]

    with st.container():
        d = {"lat": lats, "lon": longs}
        df = pd.DataFrame(data=d)
        st.map(df)

    col1, col2 = st.columns((3, 3))

    with col1:
        with st.container():
            st.subheader("Entregador")
            st.text(f"Nome : {deliveryman.get('name')}")
            st.text(
                f"Tipo de Veículo: {deliveryman.get('vehicle').split('-')[0].strip()}"
            )
            st.text(
                f"Modelo do Veículo: {deliveryman.get('vehicle').split('-')[1].strip()}"
            )

    with col2:
        with st.container():
            st.subheader("Comprador")
            st.text(f"Nome : {buyer.get('name')}")
            st.text(
                f"CEP : {'{}-{}'.format(buyer.get('cep')[:5], buyer.get('cep')[5:8])}"
            )
            st.text(
                f"CPF : {'{}.{}.{}-{}'.format(buyer.get('cpf')[:3], buyer.get('cpf')[3:6], buyer.get('cpf')[6:9], buyer.get('cpf')[9:])}"
            )

    c1, c2 = st.columns((3, 3))
    with c1:
        st.subheader("Detalhes da Compra")
        st.text(f"Identificação do Produto : {deliveryData.get('product').get('id')}")
        st.text(f"Nome do Produto : {deliveryData.get('product').get('name')}")
        st.text(f"Quantidade : {deliveryData.get('product').get('quant')}")
        st.text(f"Valor do Produto : {deliveryData.get('product').get('value')}")

    with c2:
        st.subheader("Detalhes da Entrega")
        st.text(
            f"CPF do Destinatário : {'{}.{}.{}-{}'.format(deliveryData.get('receiverCpf')[:3], deliveryData.get('receiverCpf')[3:6], deliveryData.get('receiverCpf')[6:9], deliveryData.get('receiverCpf')[9:])}"
        )

    handleShippedDelivery(
        lats,
        longs,
        deliveryData.get("statusDelivery"),
        [buyer.get("cpf"), deliveryData.get("receiverCpf")],
    )
