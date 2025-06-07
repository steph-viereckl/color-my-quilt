# Color My Quilt

This is a website I am building as a capstone project for the [100 Days of Code: The Complete Python Pro Bootcamp](https://r.search.yahoo.com/rdclks/dWU9NTFvMTAyNWs0NzdudSZ1dD0xNzQ5MjYyMDc4MTY2JnVvPTgyODA3MzU1ODIzNzIxJmx0PTImcz0xJmVzPWN0OGYueDY3UEQ4U19EQkJ5N285cjJtOVI2OF9WSmJCazlMOVB2Tzg1enBYN1hiY0pLaHhIWGlUNE5SdnNPRnlDazc1TE5Vbl96cmhLZ3Mt/RV=2/RE=1751854078/RO=14/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8ItHsvrrKFnV91CgmVVGBKjVUCUyMGg_5BmLmcTA1FRII4FfNMqVrW5FJc2Iar-qyM2fXys296ES0WrxjOJKCa4qqTAdCdMJINRYTijimVrirVxUl-kAcoelASyFtDtY6lNyHbCOr4qPcCP1bPeNSXg1z5ssg67wOtwVt6QEuGJaiZctFL8mRvVS9NcY8WwWUBh--Sg%26u%3daHR0cHMlM2ElMmYlMmZ3d3cudWRlbXkuY29tJTJmY291cnNlJTJmMTAwLWRheXMtb2YtY29kZSUyZiUzZnV0bV9zb3VyY2UlM2RiaW5nJTI2dXRtX21lZGl1bSUzZHVkZW15YWRzJTI2dXRtX2NhbXBhaWduJTNkQkctU2VhcmNoX0tleXdvcmRfQWxwaGFfUHJvZl9sYS5FTl9jYy5VUyUyNmNhbXBhaWdudHlwZSUzZFNlYXJjaCUyNnBvcnRmb2xpbyUzZEJpbmctVVNBJTI2bGFuZ3VhZ2UlM2RFTiUyNnByb2R1Y3QlM2RDb3Vyc2UlMjZ0ZXN0JTNkJTI2YXVkaWVuY2UlM2RLZXl3b3JkJTI2dG9waWMlM2RQeXRob24lMjZwcmlvcml0eSUzZEFscGhhJTI2dXRtX2NvbnRlbnQlM2RkZWFsNDU4NCUyNnV0bV90ZXJtJTNkXy5fYWdfMTMyNDkxMzg4OTY1MzY3NV8uX2FkX18uX2t3X3B5dGhvbl8uX2RlX2NfLl9kbV9fLl9wbF9fLl90aV9rd2QtODI4MDgyMTMwMTUzMDUlM2Fsb2MtMTkwXy5fbGlfNTYwNDVfLl9wZF9fLl8lMjZtYXRjaHR5cGUlM2RwJTI2bXNjbGtpZCUzZDdkOGJmZTY1OWJlMzE1ODBlNDU0OTYyNjA1MWRiODZh%26rlid%3d7d8bfe659be31580e4549626051db86a/RK=2/RS=gsEU22PAq3qO6M3oQjb_6snR.TY-;_ylt=AwrjIjT.nkNoxMwdFRoPxQt.;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZANEMjg2NjNUXzEEc2VjA292LXRvcA--;_ylc=X3IDMgRydAMw?IG=0ae32234913546968700000000394d63). 

The idea is to build a website using Python that can upload a photo of a quilt, and the program will match the quilt colors with the Kona Solids quilt fabrics that are needed in the quilt.

![Screenshot of Color My Quilt](static/assets/img/color_my_quilt_screenshot.png "Color My Quilt Demo")

## TODO

* How to store uploaded photo on client side instead of server? How do websites handle this?
* Add Kona color palette matching (i.e. show 5 related colors and let user click 1)
* Add google search to return kona fabrics in the wild?
* Will need to address colors showing up differently in different lights. Would be amazing if it could also return a google search of that fabric IRL?
* Return Kona Color Chart Group (i.e. Leaf is in group "G")
* Add ability to get "similar hex" colors
* Add ability to increase or decrease brightness of selected image?
* Improve button UI
* Add ability to toggle between hex and rgb
* Add Stripe API for funsies
* Don't show fabric tile if none are selected (currently is defualted) 
* Create a new page that is a list of the robert kaufman fabric pictures and rgb matches
* 
## Buggies

* "No file chosen" is shown as text even when image is still shown
