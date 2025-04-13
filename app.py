import streamlit as st
import fitz  # PyMuPDF
import csv

# Função para carregar nomes do CSV
def carregar_nomes(caminho_arquivo):
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row['nome'].strip().lower() for row in reader]

# Função para buscar nomes no PDF
def buscar_nomes_pdf(pdf_file, nomes, contexto=300):
    resultados = []

    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for pagina_num, pagina in enumerate(doc, start=1):
            texto = pagina.get_text()
            texto_lower = texto.lower()
            for nome in nomes:
                if nome in texto_lower:
                    idx = texto_lower.find(nome)
                    inicio = max(0, idx - contexto)
                    fim = min(len(texto), idx + contexto)
                    trecho = texto[inicio:fim].replace('\n', ' ')
                    resultados.append({
                        "nome": nome.title(),
                        "pagina": pagina_num,
                        "trecho": trecho.strip()
                    })
    return resultados

# ================= STREAMLIT APP ===================

st.set_page_config(page_title="Verificador de Nomes - Diário Oficial", layout="centered")

# TOPO DO APP
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>EMEF JOÃO DA SILVA</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: #708090;'>Desenvolvido por Guilherme Lucena</h6>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Verificação de nomes no Diário Oficial</h3>", unsafe_allow_html=True)
st.markdown("---")

# UPLOAD DO PDF
pdf_file = st.file_uploader("📄 Faça upload do Diário Oficial (PDF)", type=["pdf"])

# Lista fixa de nomes
nomes = carregar_nomes("nomes.csv")

if pdf_file is not None:
    with st.spinner("🔍 Procurando nomes no diário..."):
        resultados = buscar_nomes_pdf(pdf_file, nomes)

    if resultados:
        st.success(f"✅ Foram encontrados {len(resultados)} resultados:")
        for r in resultados:
            st.markdown(f"""
                <div style='background-color: #050505; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <strong>👤 Nome:</strong> {r['nome']}<br>
                    <strong>📄 Página:</strong> {r['pagina']}<br>
                    <strong>📝 Trecho:</strong> {r['trecho']}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔎 Nenhum nome da lista foi encontrado neste PDF.")
