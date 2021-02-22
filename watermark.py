from PIL import Image, ImageDraw, ImageFont
import io
import PySimpleGUI as sg

sg.theme("Material1")
layout = [
    [sg.T("")],
    [sg.Text("Choose a file: "), sg.Input(key="-IN2-" ,change_submits=True, size=(30,1)), sg.FileBrowse(size=(None, None), key="-IN-")],
    [sg.T("")],
    [sg.Image(size=(256,256),key="-IMAGE-"), sg.Text(size=(40, 1),key="-IM-")],
    [sg.T(""),],
    [sg.Button("Mark Image", disabled=True, key="-MARK-"), sg.Text(size=(40, 1),key='-DONE-')],
    [sg.Button("Exit")]
    ]

###Building Window
window = sg.Window('Watermarker', layout, size=(456,456),)
    
while True:
    event, values = window.read()
    
    image = Image.open(values["-IN2-"])
    width, height = image.size
    wper = int(width/1920*100)
    hper = int(height/1080*100)
    if wper < hper:
        per = wper
    else:
        per = hper
    lable= str(width) + " x " + str(height) + " - " + str(per) + "%"
    window['-IM-'].update(lable)
    image.thumbnail((256, 256))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())
    
    window['-MARK-'].update(disabled=False)
    
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "-MARK-":
        print(values["-IN-"])
        window['-DONE-'].update("marking")
        
        input_file = values["-IN-"]
        
        image = Image.open(input_file)

        width, height = image.size
        wper = int(width/1920*100)
        hper = int(height/1080*100)
        if wper < hper:
            per = wper
        else:
            per = hper
        lable= str(width) + " x " + str(height) + " - " + str(per) + "%"
        fs = int(per/4)
        f = ImageFont.truetype('Roboto-Bold.ttf', size=fs)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10),lable,font=f,fill =(150, 150, 150))

        output_file = input_file.rsplit( ".", 1 )[ 0 ]
        image.save(output_file + "_marked.png")
        window['-DONE-'].update("done")
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
