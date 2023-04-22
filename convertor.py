import os

if __name__ == '__main__':
    for i in range(2):
        for j in range(10):
            print("rain_" +str(i)+ str(j))
            arg = 'python3 read_geotiff.py -i ./data/rainTIFF/rain_' + str(i) + str(j) + ' -o rain_20' + str(i) + str(j) + '.vti'
            os.system(arg)
    
    # for i in range(2):
    for j in range(4):
        print("rain_" +str(2)+ str(j))
        arg = 'python3 read_geotiff.py -i ./data/rainTIFF/rain_' + str(2) + str(j) + ' -o rain_20' + str(2) + str(j) + '.vti'
        os.system(arg)
            
    