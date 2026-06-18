from typing_extensions import TypedDict,Annotated

class StartupProfile(TypedDict):
    """A profile for the startup state."""
    Profile_Name:Annotated[str,...,"The name of the startup profile."]
    Year_Founded:Annotated[int,...,"The year the startup was founded."]
    Description:Annotated[str,...,"A brief description of the startup."]
    Industry:Annotated[str,...,"The industry the startup operates in."]
    Target_Customer:Annotated[str,...,"The primary customer base for the startup's products or services."]
    Problem_Statement:Annotated[list[str],...,"A clear and concise statement of the problem the startup aims to solve."]
    Proposed_Solution:Annotated[str,...,"A description of the startup's proposed solution to the identified problem."]
    Business_Model:Annotated[str,...,"An explanation of how the startup plans to generate revenue and sustain its operations."] 
    Key_Features:Annotated[list[str],...,"A list of the key features or unique selling points of the startup's product or service."] 


    