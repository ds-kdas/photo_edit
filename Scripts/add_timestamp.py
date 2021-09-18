import cv2
from exif import Image
from pathlib import Path
import typer

class AddTime:
    def __init__(self,dir_path):
        self.dir_path = dir_path

    def _get_exif(self,_filename):
        try:    
            with open(_filename, "rb") as pic_file:
                image_exif = Image(pic_file)
        except:
            raise "datetime is not avaialable"
        finally:
            return image_exif.datetime
    
    def _add_text(self,img,date_info,x,y):        
        BLACK = (255,255,255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1.1
        font_color = BLACK
        font_thickness = 2
        text = date_info
        x,y = x,y
        img_text = cv2.putText(img, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
        return img_text
    
    def _get_coordinate(self,img,offset=50):
        dim = img.shape
        x = offset
        y = dim[0]-offset
        return x,y

    def _edit_pic(self):
        for im in Path(self.dir_path).iterdir():
            im = str(im)
            typer.echo("processing image "+ im)
            date_info=self._get_exif(im)
            img=cv2.imread(str(im))
            x,y = self._get_coordinate(img)
            edited_image=self._add_text(img,date_info,x,y)
            cv2.imwrite(str(im),edited_image)
            typer.echo("Saving processed image "+ im)

def main(dir_path):
    at = AddTime(dir_path)
    at._edit_pic()
    

if __name__ == "__main__":
    typer.run(main)
