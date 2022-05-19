from tkinter import YES
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import math
# import heapq as hq

Q = {(50,920):(-1,-1,0)}

def draw_obstacles(r):
    data = np.zeros((1001,1001,3), dtype=np.uint8)
    data[:,:,:] = [255]
    
    img = cv2.circle(data, (250,250), 100+r, (255,0,0), -1) #drawing a circle as an obstacle
    img = cv2.circle(data, (500,500), 100+r, (255,0,0), -1)
    img = cv2.circle(data, (750,750), 100+r, (255,0,0), -1)
    img = cv2.circle(data, (250,750), 100+r, (255,0,0), -1)
    img = cv2.circle(data, (750,250), 100+r, (255,0,0), -1)

    img = cv2.circle(data, (50,920), 50 , (0,255,0), -1) # starting point  (x,y) in BGR

    img = cv2.circle(data, (920,50), 90 , (0,0,255), -1) # end point

    return img

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def backtrack( a ,b ,img , img2):

    # x = pts[0]
    # y = pts[1]
    # print(a,b)
    bk = [(a,b)]
    while a != 50 and b != 920 :
        xn,yn,c = Q[(a,b)]        
        # print(xn,yn)
        cv2.line(img, (xn,yn), (a,b), (255,0,255), 4)
        cv2.imshow("Animation", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.line(img2, (xn,yn), (a,b), (255,0,255), 4)
        bk.append((xn/100,-yn/100))
        a = xn
        b = yn
    bk.reverse()
    print(bk)

def main():

    img = draw_obstacles(20)
    img2 = draw_obstacles(0)

    pts = [(50,920)]
    # print(Q[(5,12)])
    # exit()
    qe = 0
    combined_list = []

    gaussian= np.random.multivariate_normal([920,50],[[300000,-150000],[-150000,300000]],size = 10000)
    for i in gaussian:
        xg,yg = int(i[0]), int(i[1])
    
        if xg >= 0 and xg <= 1000 and yg >= 0 and yg <= 1000:
            combined_list.append((xg,yg))

    # print(len(combined_list))
    # print(combined_list)


    for zz in combined_list:
        
        y = zz[1]
        # y = y//10
        x = zz[0]
        # print(x,y)
        # exit()
        # x = x//10

        # cv2.circle(img,(x,y),1,(0,0,0),-1)

        if img[x,y,0] == 255 and img[x,y,1] == 0 and img[x,y,2] == 0:
            pass

        elif (x,y) not in Q:
            # print("random points",x,y)
            k = 10000
            c = 10000
            for i in pts:
                a,b = i
                d = distance((a,b),(x,y))
                if d < k:
                    k = d
                    nearestA = a
                    nearestB = b
                
            # print(k)
            if k < 3:
                continue
            
            elif k <= 8 and k > 2:      
                #put in dictionary
                pcost = Q[(nearestA,nearestB)][2]
                ncost = pcost + k
                for i in pts:
                    a,b = i
                    
                    if (a - x)**2 + (b - y)**2 <= 100:

                        if ncost + (math.sqrt((a - x)**2 + (b - y)**2)) < Q[(a,b)][2]:

                            px , py = Q[(a,b)][0], Q[(a,b)][1]
                            cv2.line(img, (a,b), (px,py), (255,255,255), 1)  #remove connection with parent

                            Q[(a,b)] = (x,y,ncost + int(math.sqrt((a - x)**2 + (b - y)**2)))
                            ## form new connection
                            cv2.line(img, (a,b), (x,y), (0,127,127), 1)
                            # print("Changing parent")
                        
                        if Q[(a,b)][2] + (math.sqrt((a - x)**2 + (b - y)**2)) < ncost:
                            ncost = Q[(a,b)][2] + (math.sqrt((a - x)**2 + (b - y)**2))
                            nearestA = a
                            nearestB = b
                                    

                Q[(x,y)] = (nearestA,nearestB,ncost)   #this is the link
                pts.append((x,y))
                cv2.line(img, (x,y), (nearestA,nearestB), (0,127,127), 1)
                cv2.circle(img,(newX,newY),1,(0,0,0),-1)
                cv2.line(img2, (x,y), (nearestA,nearestB), (0,127,127), 1)
                cv2.circle(img2,(newX,newY),1,(0,0,0),-1)
                cv2.imshow("Animation", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if img[x,y,0] == 0 and img[x,y,1] == 255 and img[x,y,2] == 0:
                    print("Goal Found")
                    # print(x,y)
                    # print(img[x,y,:])
                    backtrack(x,y,img, img2)
                    break                

            else:

                newX = int(nearestA + (8/k)*(x - nearestA))
                newY = int(nearestB + (8/k)*(y - nearestB))
                if (newX,newY) not in pts and distance((newX,newY),(nearestA,nearestB)) > 3:
                    if (newX, newY) not in pts:
                        if img[newX,newY,0] == 255 and img[newX,newY,1] == 0 and img[newX,newY,2] == 0:
                            pass
                        else:
                            _, _,pcost = Q[(nearestA,nearestB)]

                            ncost = pcost + k
                            ######reduce the cost of surrounding cells
                            for i in pts:
                                a,b = i
                                
                                if (a - newX)**2 + (b - newY)**2 <= 36:
                                    if ncost + (math.sqrt((a - newX)**2 + (b - newY)**2)) < Q[(a,b)][2]:
                                        print(ncost + int(math.sqrt((a - newX)**2 + (b - newY)**2)))
                                        print(Q[(a,b)][2])
                                        
                                        px , py = Q[(a,b)][0], Q[(a,b)][1]
                                        cv2.line(img, (a,b), (px,py), (255,255,255), 1)  #remove connection with parent

                                        Q[(a,b)] = (newX, newY,ncost + int(math.sqrt((a - newX)**2 + (b - newY)**2)))
                                        ## form new connection
                                        cv2.line(img, (a,b), (newX,newY), (0,127,127), 1)
                                        print("Parent ", px,py)
                                        print("child ", a,b)
                                        print("new Parent ",newX, newY )
                                
                                    if Q[(a,b)][2] + (math.sqrt((a - newX)**2 + (b - newY)**2)) < ncost:
                                        ncost = Q[(a,b)][2] + (math.sqrt((a - newX)**2 + (b - newY)**2))
                                        nearestA = a
                                        nearestB = b
                                                

                            Q[(newX,newY)] = (nearestA,nearestB,ncost)
                            pts.append((newX,newY)) 
                            cv2.line(img, (nearestA,nearestB), (newX,newY), (0,127,127), 1)
                            cv2.circle(img,(newX,newY),1,(0,0,0),-1)
                            
                            cv2.line(img2, (newX,newY), (nearestA,nearestB), (0,127,127), 1)
                            cv2.circle(img2,(newX,newY),1,(0,0,0),-1)
                            
                            cv2.imshow("Animation", img)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    
                            if img[newX,newY,0] == 0 and img[newX,newY,1] == 255 and img[newX,newY,2] == 0 or img[newX+1,newY+1,0] == 0 and img[newX+1,newY+1,1] == 255 and img[newX+1,newY+1,2] == 0:
                                print("Goal Found")
                                # print(newX,newY)
                                # print(img[newX,newY,:])
                                backtrack(newX,newY,img, img2)
                                break




    # print(Q)
    print(qe)
    plt.imshow(img2)
    plt.show()

    # cv2.imshow("Final Path", img)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()