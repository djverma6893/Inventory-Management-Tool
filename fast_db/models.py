from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated,Optional

class User(BaseModel):
    name: str
    email: str

# class UserCreate(BaseModel):
#     team_member: Annotated[str, Field(min_length=1, max_length=50, discriminator="Enter your team member name")]
#     laptop1_sn: Annotated[str, Field(default=None, min_length=1, max_length=50, discriminator="Enter your laptop serial number")]
#     laptop2_sn: Annotated[str, Field(default=None, max_length=50, discriminator="Enter your laptop serial number")]
#     intern_phone: Annotated[str, Field(default=None, min_length=1, max_length=50, discriminator="Enter your intern phone serial number")]
#     test_phone1:  Annotated[str, Field(default=None, max_length=50, discriminator="Enter your test phone serial number")]
#     test_phone2:  Annotated[str, Field(default=None, max_length=50, discriminator="Enter your test phone serial number")]
#     hcl_laptop:  Annotated[str, Field(default=None, max_length=50, discriminator="Enter yes if you have hcl laptop ")]
#     serial_no: Annotated[str, Field(default=None, max_length=50, discriminator="Enter your Hcl Laptop serial number")]
#
#     @model_validator(mode = "after")
#     def hcl_laptop_validator(self):
#         if self.hcl_laptop == 'Yes' and self.serial_no is None:
#             raise ValueError('Please enter your Hcl Laptop serial number')
#         else:
#             return self

# class UserResponce(BaseModel):



class UserCreate(BaseModel):
    team_member: str = Field(..., min_length=1, max_length=50, description="Enter your team member name")

    laptop1_sn: Optional[str] = Field(None, min_length=1, max_length=50, description="Enter your laptop serial number")
    laptop2_sn: Optional[str] = Field(None, max_length=50, description="Enter your laptop serial number")

    intern_phone: Optional[str] = Field(None, min_length=1, max_length=50, description="Enter your intern phone serial number")

    test_phone1: Optional[str] = Field(None, max_length=50, description="Enter your test phone serial number")
    test_phone2: Optional[str] = Field(None, max_length=50, description="Enter your test phone serial number")

    hcl_laptop: str = Field(..., max_length=50, description="Enter Yes if you have HCL laptop")

    serial_no: Optional[str] = Field(None, max_length=50, description="Enter your HCL Laptop serial number")

    @model_validator(mode="after")
    def hcl_laptop_validator(self):
        if self.hcl_laptop == "Yes" and not self.serial_no:
            raise ValueError("Please enter your HCL Laptop serial number")
        return self
