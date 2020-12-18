import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem

from requests import get, put, post, delete

from info import URL

 
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)

        '''self.del_o.clicked.connect(self.delette_product_operation)
        self.add_o.clicked.connect(self.add_product_operation)

        self.del_a.clicked.connect(self.delette_product_additional)
        self.add_a.clicked.connect(self.add_product_additional)

        self.del_p.clicked.connect(self.delette_product_part)
        self.add_ex.clicked.connect(self.add_existing_part)
        self.crt_new.clicked.connect(self.create_add_part)'''

        self.product_a.triggered.connect(self.create_prod)

        self.act.clicked.connect(self.product_upd)

        self.load(1)

    def create_prod(self):
        post(URL + f'/api/product/0?title=ПРОДУКТ&r_coef=0.0&r_cost=1&w_cost=1')
        product_id = get(URL + '/api/products?ids=all').json()['result']['products'][-1]['id']
        self.ID.setText(str(product_id))
        self.load(product_id)

    def product_upd(self):
        id = self.ID.text()

        title = self.name.text()
        r_coef = self.profitability.text()
        if not r_coef:
            r_coef = 0.0
        
        put(URL + f'/api/product/{id}?title={title}&r_coef={r_coef}')
        get(URL + f'/api/productcost/{id}')

        self.load(id)
    
    def load(self, p_id):
        print(URL + f'/api/product/{p_id}')
        response = get(URL + f'/api/product/{p_id}')
        print(response)
        if not response:
            self.create_prod()
            return

        self.operations_list.clear()
        self.additionals_list.clear()
        self.parts_list.clear()

        product_info = response.json()['result']['product']

        self.ID.setText(str(product_info['id']))

        self.name.setText(product_info['title'])
        self.r_cost.setText(str(product_info['retale cost']))
        self.w_cost.setText(str(product_info['wholesale cost']))
        self.profitability.setText(str(product_info['profitability']))

        for add in product_info['additionals']:
            item = QListWidgetItem(f"{add['title']} x{add['count']}")
            item.setData(Qt.UserRole, add['id'])
            self.additionals_list.addItem(item)
        
        for oper in product_info['operations']:
            item = QListWidgetItem(f"{oper['title']}; время {oper['time']} ч.")
            item.setData(Qt.UserRole, oper['id'])
            self.operations_list.addItem(item)
        
        for part in product_info['parts']:
            item = QListWidgetItem(part['title'])
            item.setData(Qt.UserRole, part['id'])
            self.parts_list.addItem(item)


descktop_app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(descktop_app.exec_())