import getopt
import sys
import os
from shutil import copyfile

def convertGLTF(file,dir_path,subdir):
    
    new_file = 'basisGLTF.gltf'
    dest = os.path.join(subdir, file)
    dest_new = os.path.join(subdir, new_file)
    read_obj = open(dest, 'r')
    write_obj = open(dest_new, 'w')
    foundImage = False
    foundTexture = False
    
    for line in read_obj:
        writeLine = True
        if '"images"' in line:                    
            foundImage = True

        if '"textures"' in line:
            foundTexture = True

        if foundTexture:
                
            if "]," in line:
                foundTexture = False
                    
            if "name" in line:
                splitted = line.split(":")
                fileBase = os.path.splitext(splitted[1])[0]
                replacedLine = line.replace(splitted[1],fileBase + '.basis" \n')
                write_obj.write(replacedLine)
                writeLine = False
           
        if foundImage:
                
            if "]," in line:
                foundImage = False
                    
            if "uri" in line:
                splitted = line.split(":")
                fileBase = os.path.splitext(splitted[1])[0]
                replacedLine = line.replace(splitted[1],fileBase + '.basis" \n')
                write_obj.write(replacedLine)
                writeLine = False
            if "mimeType" in line:
                splitted = line.split(":")
                replacedLine = line.replace("image/png","image/basis")
                write_obj.write(replacedLine)
                writeLine = False
                

        if writeLine:
            write_obj.write(line)


    read_obj.close()
    write_obj.close()
    #remove old gtf without basis
    os.remove(dest)
    #rename new gltf like the old one
    os.rename(dest_new, dest)
    
                    


def imageToBasis(file,dir_path,subdir):
    dest = os.path.join(subdir, file)
    cmd = 'basisu ' + dest
    print(cmd)
    fileName = os.path.splitext(file)[0] + '.basis'
    os.system(cmd) # returns the exit status
    copyfile(os.path.join(dir_path, fileName), os.path.join(subdir, fileName))
    os.remove(os.path.join(dir_path,fileName))
    os.remove(os.path.join(subdir,file))

def main():

    folder = ''

    try:
        opts, args = getopt.getopt(sys.argv,'hd:')
    except getopt.GetoptError:
        print('basis_encoder.py -d <gltfDirectory>')
    
    print(opts)
    print(args)


    dir_path = os.path.dirname(os.path.realpath(__file__))

    for subdir, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                print("converting image")
                imageToBasis(file,dir_path,subdir)
            if file.endswith('.gltf'):
                print("converting gltf")
                convertGLTF(file,dir_path,subdir)

                


    



if __name__ == "__main__":
    main()
