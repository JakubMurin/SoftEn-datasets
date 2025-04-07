from lxml import etree
from io import StringIO
import os

data_path = r"C:\Users\Jakub\SoftEn-datasets\data"
dtd_scheme_path = r"C:\Users\Jakub\SoftEn-datasets\data\schemas\usecase.dtd"
xsd_scheme_path = r"C:\Users\Jakub\SoftEn-datasets\data\schemas\usecase.xsd"

class XmlValidation:
    
    _green_checkmark = u"\033[0;32m\u2713\033[00m"
    _red_cross = u"\033[0;31m\u2717\033[00m"
    
    def __init__(self, validation_schema_path: str|None = None):
        if validation_schema_path is None:
            return
        
        file_extension = validation_schema_path.split(".")[-1]
        if file_extension == "dtd":
            self.schema = etree.DTD(validation_schema_path)
            self.schema_type = "DTD"
            
        elif file_extension == "xsd":
            self.schema = etree.XMLSchema(etree.parse(validation_schema_path))
            self.schema_type = "XSD"
            
        else:
            raise ValueError(f"Wrong file type! Expected dtd or xsd, got {file_extension}.")


    def validate_file(self, file_path: str, custom_validation: bool = False) -> bool:
        try:
            print("\nValidating file:", file_path)
            xml_tree = etree.parse(file_path)
        
            if custom_validation:
                result = self.custom_scheme.validate(xml_tree)
            else:
                result = self.schema.validate(xml_tree)
        
            if result:
                print(self._green_checkmark, f"valid file against {'custom ' if custom_validation else ''}{self.schema_type} schema")
                return True

            print(self._red_cross, f"XML {file_path} is invalid against {'custom ' if custom_validation else ''}{self.schema_type} schema.\n{self.schema.error_log}")
            return False
                
        except etree.XMLSyntaxError as e:
            print(f"Error while parsing XML {file_path}: {e}")
    
    def set_custom_scheme(self, mainSteps=None):

        dtd_template=f"""
            <!ELEMENT useCase (name, description?, actors?, preconditions?, successEndConditions?, failureEndConditions?, trigger?, mainSequence, alternativeSteps?, errorSteps?)>
            <!ATTLIST useCase id CDATA   #REQUIRED>

            <!ELEMENT name (#PCDATA)>
            <!ELEMENT description (#PCDATA)>
            <!ELEMENT actors (actor+)>
            <!ELEMENT actor (#PCDATA)>
            <!ELEMENT preconditions (precondition+)>
            <!ELEMENT precondition (#PCDATA)>
            <!ELEMENT successEndConditions (condition+)>
            <!ELEMENT condition (#PCDATA)>
            <!ELEMENT failureEndConditions (condition+)>
            <!ELEMENT trigger (#PCDATA)>

            <!ELEMENT mainSequence ({"step+" if mainSteps is None else (mainSteps * "step,")[:-1]})>
            <!ELEMENT alternativeSteps (asteps+)>
            <!ELEMENT errorSteps (esteps+)>

            <!ELEMENT asteps (step+)>
            <!ATTLIST asteps id ID #REQUIRED start IDREF #REQUIRED continue IDREF #IMPLIED>

            <!ELEMENT esteps (description?, step+)>
            <!ATTLIST esteps id ID #REQUIRED start IDREF #REQUIRED>

            <!ELEMENT step (#PCDATA)>
            <!ATTLIST step id ID #REQUIRED>

            <!ELEMENT description (#PCDATA)>
        """
        # print(dtd_template)
        self.custom_scheme = etree.DTD(StringIO(dtd_template))



def get_all_files(path: str, folder_name: str) -> list[str]:
    folder_path = os.path.join(path, folder_name)
    files = os.listdir(folder_path)
    xml_files = filter(lambda p: p.endswith(".xml"), files)
    return list(map(lambda p: os.path.join(folder_path, p), xml_files))

if __name__ == "__main__":
    
    validator = XmlValidation(dtd_scheme_path)
    # validator.set_custom_scheme()
    validator.validate_file(r"C:\Users\Jakub\SoftEn-datasets\data\usecases\04.xml")

    # for file_path in get_all_files(data_path, "usecases"):
    #     validator.validate_file(file_path)