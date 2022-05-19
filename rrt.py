import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import math
# import heapq as hq

Q = {(5,12):(-1,-1)}

def draw_obstacles():
    data = np.zeros((501,501,3), dtype=np.uint8)
    data[:,:,:] = [255]
    
    img = cv2.circle(data, (25,25), 10, (255,0,0), -1) #drawing a circle as an obstacle
    img = cv2.circle(data, (50,50), 10, (255,0,0), -1)
    img = cv2.circle(data, (75,75), 10, (255,0,0), -1)
    img = cv2.circle(data, (25,75), 10, (255,0,0), -1)
    img = cv2.circle(data, (75,25), 10, (255,0,0), -1)

    img = cv2.circle(data, (5,92), 5 , (0,255,0), -1) # starting point  (x,y) in BGR

    img = cv2.circle(data, (92,5), 9 , (0,0,255), -1) # end point

    return img

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def backtrack( a ,b ,img):

    # x = pts[0]
    # y = pts[1]
    print(a,b)
    while a != 5 and b != 92 :
        xn,yn = Q[(a,b)]        

        cv2.line(img, (xn,yn), (a,b), (255,0,255), 1)
        a = xn
        b = yn

def main():

    img = draw_obstacles()
    pts = [(5,92)]
    qe = 0
    while qe < 1000:
        
        y = random.randint(0, 500)
        # y = y//10
        x = random.randint(0, 500)
        # print(x,y)
        # x = x//10
        if img[x,y,0] == 255 and img[x,y,1] == 0 and img[x,y,2] == 0:
            pass

        elif (x,y) not in Q:
            # print("random points",x,y)
            k = 10000
            
            for i in pts:
                a,b = i
                d = distance((a,b),(x,y))
                if d < k:
                    k = d
                    nearestA = a
                    nearestB = b

            if k < 2:
                continue
            
            elif k <= 6 and k > 2:      
                #put in dictionary
                Q[(x,y)] = (nearestA,nearestB) 
                pts.append((x,y))
                cv2.line(img, (x,y), (nearestA,nearestB), (0,127,127), 1)
                cv2.circle(img,(x,y),1,(0,0,0),-1)
                cv2.imshow("Animation", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if img[x,y,0] == 0 and img[x,y,1] == 255 and img[x,y,2] == 0:
                    print("Goal Found")
                    # print(x,y)
                    # print(img[x,y,:])
                    backtrack(x,y,img)
                    break                

            else:
                newX = int(nearestA + (6/k)*(x - nearestA))
                newY = int(nearestB + (6/k)*(y - nearestB))
                if (newX,newY) not in pts and distance((newX,newY),(nearestA,nearestB)) > 3:
                    if (newX, newY) not in pts:
                        if img[newX,newY,0] == 255 and img[newX,newY,1] == 0 and img[newX,newY,2] == 0:
                            pass
                        else:
                            Q[(newX,newY)] = (nearestA,nearestB)
                            pts.append((newX,newY)) 
                            cv2.line(img, (nearestA,nearestB), (newX,newY), (0,127,127), 1)
                            cv2.circle(img,(newX,newY),1,(0,0,0),-1)
                            cv2.imshow("Animation", img)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    
                            if img[newX,newY,0] == 0 and img[newX,newY,1] == 255 and img[newX,newY,2] == 0:
                                print("Goal Found")
                                # print(newX,newY)
                                # print(img[newX,newY,:])
                                backtrack(newX,newY,img)
                                break



        qe += 1
    print(qe)
    plt.imshow(img)
    plt.show()
    # cv2.imshow("Final Path", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()