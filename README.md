# Roy G Biv

This python module is intended to provide a set of image analysis tools. This is very much a work in progress...

_by Giv Parvaneh_

## Usage

	from roygbiv import *
	roy = Roygbiv('myimage.png')
    
    roy.get_average_color('hex')
    #3e453f
    
    roy.get_average_color('rgb')
    (12,200,138)

