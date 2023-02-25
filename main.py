import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QFont, QIcon
from PyQt5.QtCore import Qt, QMimeData
from PyPDF2 import PdfReader, PdfWriter
from datetime import date

class DragAndDropWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Configura a janela
        self.setAcceptDrops(True)
        self.setWindowTitle('Livroware')
        self.setWindowIcon(QIcon('system\img\logo.png'))

        self.label = QLabel("Arraste e solte \num arquivo aqui")
        self.label.setFont(QFont('Courier New', 15))
        self.label.setAlignment(Qt.AlignCenter)

        self.botao = QPushButton('Imprimir')
        self.botao.setFont(QFont('Courier New', 8))
        self.botao.setVisible(False)
        self.botao.clicked.connect(self.executar)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.botao)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                file_path = str(url.toLocalFile())
                self.caminho = file_path
                self.botao.setVisible(True)

    def executar(self):
        print(self.caminho)
        try:
            with open(self.caminho, 'rb') as arquivo:
                # Criar um objeto PDFReader
                leitor = PdfReader(arquivo)

                paginas = []
                # Iterar por todas as páginas do PDF
                for page_num in range(len(leitor.pages)):
                    # Obter a página atual
                    page = leitor.pages[page_num]
                    paginas.append(leitor.pages[page_num])

                nova_ordem = [1, 3, 2] # exemplo de nova ordem de páginas
                paginas_ordenadas = [paginas[i-1] for i in nova_ordem]

                escritor = PdfWriter()
                for pagina in paginas_ordenadas:
                    escritor.add_page(pagina)

                with open(f'log/pdf_{date.today()}.pdf', 'wb') as novo_arquivo:
                    escritor.write(novo_arquivo)

            self.close
        except:
            print('Não foi possivel executar')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DragAndDropWidget()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec_())


# Extrair o conteúdo do texto da página
#text = page.extract_text()
# Imprimir o conteúdo do texto da página
#print(text)