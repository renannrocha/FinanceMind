import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO
import io
import os
from utils.graficos import gerar_grafico_despesas, gerar_grafico_receitas, gerar_grafico_transacoes

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório Financeiro', 0, 1, 'C')

    def add_figure(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        self.image(buf, x=10, y=None, w=180)

def exportar_para_pdf(inicio, fim):
    try:
        pdf = PDF()
        pdf.add_page()

        # Adiciona título
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório de Finanças: {inicio} a {fim}", ln=True, align='C')

        # Gera os gráficos
        try:
            fig_despesas = gerar_grafico_despesas()
            fig_receitas = gerar_grafico_receitas()
            fig_transacoes = gerar_grafico_transacoes()
        except Exception as e:
            print(f"Erro ao gerar gráficos: {e}")
            return

        # Salva os gráficos em arquivos temporários
        file_paths = []
        for i, fig in enumerate([fig_despesas, fig_receitas, fig_transacoes]):
            file_path = f"temp_graph_{i}.png"
            try:
                fig.savefig(file_path, format='png')
                file_paths.append(file_path)
            except Exception as e:
                print(f"Erro ao salvar gráfico {i}: {e}")
                return

        # Adiciona gráficos ao PDF
        for file_path in file_paths:
            try:
                pdf.add_page()
                pdf.image(file_path, x=10, y=None, w=180)
                os.remove(file_path)  # Remove o arquivo temporário após adicionar ao PDF
            except Exception as e:
                print(f"Erro ao adicionar imagem {file_path} ao PDF: {e}")
                continue  # Ignora o erro e continua com o próximo gráfico

        # Salva o PDF
        pdf_output_path = "relatorio_financeiro.pdf"
        try:
            pdf.output(pdf_output_path)
            print(f"PDF salvo em {pdf_output_path}")
        except Exception as e:
            print(f"Erro ao salvar o PDF: {e}")

    except Exception as e:
        print(f"Erro ao exportar para PDF: {e}")

# Exemplo de uso da função
if __name__ == "__main__":
    exportar_para_pdf('2024-01-01', '2024-12-31')
