import Image, ImageChops, os, glob, ImageFont, ImageDraw




def speed():
    CalibrationFactor = 4.21#128.8
    Unit = "MPH"


    box = (113,200,761,489)
    TestSensitivity = 1

    Sensitivity = 90




    filelist = []
    fileMS = []
    fileS = []
    fileM = []
    fileH = []
    for infile in glob.glob('motion*'):
        filelist = filelist + [infile]
       
        fileMS = fileMS + [infile[27:30]]
        fileS = fileS + [infile[24:26]]
        fileM = fileM + [infile[21:23]]
        fileH = fileH + [infile[18:20]]


    FileCount = len(filelist)
    if float(FileCount)/float(3)-int(FileCount/3) <> 0:
        print 'The number of files is not divisible by 3.'
        print 'Photo software must be set to capture 3 images'
        print 'each time motion is detected.'
        h = raw_input('press enter to quit')
        raise NameError('Number of files not divisible by 3')

    #print('Reached 1')



    for x in range(1,(FileCount/3+1)):
       # print('Reached 3')
        a = x*3-3
        b = x*3-2
        c = x*3-1
        #Start = int(fileMS[b])+int(fileS[b])*1000+int(fileM[b])*60000+int(fileH[b])*3600000
        #End = int(fileMS[c])+int(fileS[c])*1000+int(fileM[c])*60000+int(fileH[c])*3600000
        #print 'Start = %d' %Start
       # print 'End = %d' %End
       # Time = End - Start
        #if Time <0:
           #    Time = End + (3600000*24) - Start
        Time = 70
        print Time
        # Converts to greyscale and crops 
        im1 = (Image.open(filelist[a]).convert("L")).crop(box)
        im2 = (Image.open(filelist[b]).convert("L")).crop(box)
        im3 = (Image.open(filelist[c]).convert("L")).crop(box)

        diff2 = ImageChops.difference(im1, im2)
        diff3 = ImageChops.difference(im1, im3)
        
        Pic2 = ImageChops.invert(Image.eval(diff2, lambda px: px <= Sensitivity and 255 or 0))
        Pic3 = ImageChops.invert(Image.eval(diff3, lambda px: px <= Sensitivity and 255 or 0))
        


        
        # Saves copies of the above photos if needed for testing.
        if TestSensitivity == 1:
            Pic2.save("Test2_" + filelist[b], quality=100)
            Pic3.save("Test3_" + filelist[b], quality=100)

           

        
        L = Pic2.getbbox()[0] - Pic3.getbbox()[0]
        R = Pic3.getbbox()[2] - Pic2.getbbox()[2]
        print 'L is = %i' %L
        print 'R is = %i' %R
        #print(L)
        #print(R)
        Speed = max(L,R)

        
              
        Vel = ("%.1f" % (float(Speed)/float(Time)*CalibrationFactor))
        txt =  str(Vel + " " + Unit)
        print(txt)


       
        
        picTxt = Image.open(filelist[b])
        saveName = "Velocity_" + filelist[b][7:100]
        draw = ImageDraw.Draw(picTxt)   
        draw.text((175,222), txt)
        picTxt.save(saveName, quality=100)

speed()

