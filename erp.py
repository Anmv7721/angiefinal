#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/png;base64,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"  # Asegúrate de poner la ruta correcta

# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_MMC_CONSTRUCCIONES")

# Variables de autenticación
USER = "Anmv"
PASSWORD = "Angie7721$"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
