from lxml import etree
from io import StringIO
from dataclasses import dataclass
import os

from utils import *

WORKING_DIR = os.getcwd()
DATA_PATH = os.path.join(WORKING_DIR, "data")
DTD_SCHEME_PATH = os.path.join(WORKING_DIR, "data\\schemas\\usecase.dtd")
XSD_SCHEME_PATH = os.path.join(WORKING_DIR, "data\\schemas\\usecase.xsd")

@dataclass
class XmlParams:
    title: str = ""
    actors: int = 0
    num_of_steps: int = 0
    num_of_alt_scenarions: int = 0
    num_of_err_scenarions: int = 0
    

class XmlValidation:
    
    _green_checkmark = u"\033[0;32m\u2713\033[00m"
    _red_cross = u"\033[0;31m\u2717\033[00m"
    
    def __init__(self, validation_schema_path: str|None = None, show_log: bool=False):
        self.show_log = show_log
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


    def validate_file(self, file_path: str, custom_validation: bool=False) -> bool | XmlParams:
        if self.show_log:
            print("\nValidating file:", file_path)
        with open(file_path, "r") as file:
            usecase = file.read()
        try:
            result = self.validate(usecase, custom_validation)
        except etree.XMLSyntaxError:
            if self.show_log:
                print(f"Error while parsing XML: {file_path}")
        return result
        
    def validate(self, usecase: str, custom_validation: bool=False) -> bool | XmlParams:
        try:
            xml_tree = etree.fromstring(usecase.encode())
        
            if custom_validation:
                result = self.custom_scheme.validate(xml_tree)
            else:
                result = self.schema.validate(xml_tree)
        
            if result:
                if self.show_log:
                    print(self._green_checkmark, f"valid file against {'custom ' if custom_validation else ''}{self.schema_type} schema")
                return self.get_params(xml_tree)

            if self.show_log:
                print(self._red_cross, f"XML is invalid against {'custom ' if custom_validation else ''}{self.schema_type} schema.\n{self.schema.error_log}")
            return False
                
        except etree.XMLSyntaxError as e:
            print(f"Error while parsing XML: {e}")
                
    def get_params(self, xml_tree: etree.ElementBase) -> XmlParams:
        title_el = xml_tree.find("name")
        title = title_el.text if title_el is not None else ""
        
        actors_el = xml_tree.find("actors")
        num_of_actors = len(actors_el) if actors_el is not None else 0
        
        steps_el = xml_tree.find("mainSequence")
        num_of_steps = len(steps_el) if steps_el is not None else 0
        
        alt_steps_el = xml_tree.find("alternativeSteps")
        num_of_alt_scenarions = len(alt_steps_el) if alt_steps_el is not None else 0
        
        err_steps_el = xml_tree.find("errorSteps")
        num_of_err_scenarions = len(err_steps_el) if err_steps_el is not None else 0
        
        if self.show_log:
            print(f"name: {title}, actors: {num_of_actors}, steps: {num_of_steps}, alt: {num_of_alt_scenarions}, err: {num_of_err_scenarions}")
        return XmlParams(title, num_of_actors, num_of_steps, num_of_alt_scenarions, num_of_err_scenarions)
    
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

if __name__ == "__main__":
    
    validator = XmlValidation(DTD_SCHEME_PATH, True)
    # validator.set_custom_scheme()
    # print(validator.validate_file(os.path.join(WORKING_DIR, "data\\usecases\\07.xml")))
    
    a="""<useCase id="1">
    <name>Resource Management</name>
    <description>Manage resources in the system</description>
    <actors>
        <actor>Administrator</actor>
        <actor>Resource Manager</actor>
    </actors>
    <preconditions>
        <precondition>System must be running</precondition>
    </preconditions>
    <successEndConditions>
        <condition>Resources managed successfully</condition>
    </successEndConditions>
    <failureEndConditions>
        <condition>Unable to manage resources</condition>
    </failureEndConditions>
    <trigger>Resource request received</trigger>
    <mainSequence>
        <step>RegisterResourceRequest</step>
        <step>RegisterResourceEvent</step>
        <step>CheckRequest</step>
        <step>CheckResponse</step>
        <step>DiffRequest</step>
        <step>DiffResponse</step>
        <step>SameStep</step>
        <step>done</step>
        <step>RegisterResourceResponse</step>
    </mainSequence>
</useCase>"""
    print(validator.validate(a))

    # for file_path in get_all_files(DATA_PATH, "usecases"):
    #     validator.validate_file(file_path)