from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from django.http import HttpResponse

def pdf_dw(text):                                  

    # Create the HttpResponse object 
    response = HttpResponse(content_type='application/pdf') 

    # This line force a download
    response['Content-Disposition'] = 'attachment; filename="1.pdf"' 

    # READ Optional GET param
    # text = request.GET.get('name', 'World')

    # Generate unique timestamp
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    p = canvas.Canvas(response)

    # Write content on the PDF 
    p.drawString(100, 500, "Hello " + text + " (Dynamic PDF) - " + ts ) 

    # Close the PDF object. 
    p.showPage() 
    p.save() 

    # Show the result to the user    
    return response