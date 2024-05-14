from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from projet_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QLabel
from PyQt5 import QtCore
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the user interface defined in projet_ui.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect the button click event to the display_images_from_database method
        self.ui.Display_Image_From_Database.clicked.connect(self.display_images_from_database)
        #self.ui.Browse_Image.clicked.connect(self.browse_image)
        # Connecter le signal cellClicked à la méthode display_selected_image
        self.ui.tableWidget_Image.cellClicked.connect(self.display_selected_image)

    
        
    def display_selected_image(self, row, column):
        # Récupérer l'objet QLabel à partir de la cellule sélectionnée
        cell_widget = self.ui.tableWidget_Image.cellWidget(row, column)
        if isinstance(cell_widget, QLabel):
            # Récupérer la pixmap de l'objet QLabel
            pixmap = cell_widget.pixmap()
            

            # Afficher la pixmap dans le widget QLabel label
            self.ui.label.setPixmap(pixmap)

    def display_images_from_database(self):
        print("Bonjour click")  # Print a message to console indicating the button click event
        
        try:
            # Connect to the database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="editimages"
            )

            # Retrieve data from the database
            cursor = mydb.cursor()
            cursor.execute("SELECT nom, image FROM Images_to_manipulate")
            rows = cursor.fetchall()

            # Display data in the tableWidget_Image
            row_position = 0
            for row in rows:
                nom, image_blob = row
                item_nom = QTableWidgetItem(nom)

                # Create a QLabel widget to display the image
                label = QLabel()
                pixmap = QPixmap()
                pixmap.loadFromData(image_blob)
                label.setScaledContents(True)

                
                label.setPixmap(pixmap)  # Adjust the size of the image if necessary
                label.setAlignment(QtCore.Qt.AlignCenter)
                  # Add border to the label


                self.ui.tableWidget_Image.setRowCount(row_position + 1)
                window.ui.tableWidget_Image.setRowHeight(row_position + 1,200)





                # Add the QLabel widget to the cell of the table
                self.ui.tableWidget_Image.setCellWidget(row_position, 1, label)
                

                # Add the image name to the first column of the table
                self.ui.tableWidget_Image.setItem(row_position, 0, item_nom)

                row_position += 1

            # Close the connection to the database
            mydb.close()
        except Exception as e:
            # Display an error message box
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("An error occurred while displaying images from the database.")
            error_message.setInformativeText(f"Error : {str(e)}")
            error_message.setWindowTitle("Error")
            error_message.exec_()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    
    # Set column widths for the tableWidget_Image
    window.ui.tableWidget_Image.setColumnWidth(0, 340)
    window.ui.tableWidget_Image.setColumnWidth(1, 100)
    
    window.show()
    app.exec_()
