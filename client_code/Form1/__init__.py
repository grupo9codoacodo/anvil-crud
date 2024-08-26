
    # Any code you write here will run before the form opens.
from ._anvil_designer import Form1Template
import anvil.server

class Form1(Form1Template):

    def __init__(self, **properties):
        # Inicializar los componentes del formulario
        self.init_components(**properties)
        # Cargar la lista de empleados al inicio
        self.refresh_data()

    def refresh_data(self):
        """Carga los datos desde la base de datos"""
        self.repeating_panel_1.items = anvil.server.call('get_employees')

    def button_add_click(self, **event_args):
        """Agregar un nuevo empleado"""
        name = self.text_box_name.text
        position = self.text_box_position.text
        salary = self.number_box_salary.value
        
        # Llamar al servidor para agregar empleado
        anvil.server.call('add_employee', name, position, salary)
        self.refresh_data()

    def button_update_click(self, **event_args):
        """Actualizar empleado seleccionado"""
        selected_row = self.repeating_panel_1.selected_item
        if selected_row:
            anvil.server.call('update_employee', selected_row['id'], self.text_box_name.text,
                              self.text_box_position.text, self.number_box_salary.value)
            self.refresh_data()

    def button_delete_click(self, **event_args):
        """Eliminar empleado seleccionado"""
        selected_row = self.repeating_panel_1.selected_item
        if selected_row:
            anvil.server.call('delete_employee', selected_row['id'])
            self.refresh_data()