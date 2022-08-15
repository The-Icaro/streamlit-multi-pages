def data_selectbox_builder(data: list):

    select_box_data = []

    for detail in data:
        select_box_data.append(f"{detail.get('id')} - {detail.get('name')}")

    return select_box_data


def delivery_selectbox_buider(delivery: list):

    select_box_data = []

    for data in delivery:
        select_box_data.append(
            f"{data.get('id')} - Entregador : {data.get('deliveryman').get('name')} | \
                                Comprador: {data.get('buyer').get('name')} | \
                                Status Entrega: {data.get('statusDelivery')}"
        )

    return select_box_data
