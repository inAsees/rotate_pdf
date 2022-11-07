import PyPDF2
from flask_restful import Resource, reqparse
from PyPDF2.errors import PdfReadError
import os
#Post parsers
post_parser = reqparse.RequestParser()
post_parser.add_argument('angle_of_rotation', type=int, required=True, help="Angle of rotation is required")
post_parser.add_argument('page_number', type=int, required=True, help="Page number is required")
post_parser.add_argument('file_path', type=str, required=True, help="File path is required")


class RotatePage(Resource):
    def post(self):
        args = post_parser.parse_args()
        angle_of_rotation = args['angle_of_rotation']
        page_number = args['page_number']
        file_path = args['file_path']
        
        # Check if file path is valid
        if not os.path.exists(file_path):
            return {
                'error': 'Invalid file path'
            }, 400
        
        
        if angle_of_rotation > 360:
            return {
                'error': 'Angle of rotation should be less than 360 degree'
            }, 400
         
        # Check if angle of rotation is multiple of 90    
        elif angle_of_rotation not in [90, 180, 270]:
            return {
                'error': 'Angle of rotation must be in multiples of 90.'
            }, 400
        
        
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                pdf_writer = PyPDF2.PdfFileWriter()
                
                total_pages = pdf_reader.getNumPages()

                # check if page number is present in the pdf file 
                if page_number not in range(1, total_pages + 1):
                    return {
                        'error':'Given page number not present in pdf file'
                        }, 400
                
   
                for page_num in range(total_pages):
                    page = pdf_reader.getPage(page_num) 
                    
                    if page_num + 1 == page_number:
                        page.rotateClockwise(angle_of_rotation)
                        pdf_writer.addPage(page)
                        continue
                    
                    pdf_writer.addPage(page)
                    
                pdf_out = open('rotated.pdf', 'wb')
                pdf_writer.write(pdf_out)
                
                return {
                    'message': 'Page rotated successfully and pdf file saved in current directory with name "rotated.pdf" '
                }, 200
                
        except PdfReadError as e:
            print(e)
            return {
                'error': 'Only pdf files are accepted'
                }, 400
            