import cv2
import numpy as np

class Mask():
    def __init__(self, img):
        self.image = img.copy()
        self.polygon_remove = []
        self.polygon_protect = []
        self.mask_remove = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.mask_protect = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    def Draw_polygon(self, text = 'image'):
        img = self.image.copy()
        list_polygon = []
        polygon = []
        def Draw_line(event, x, y, flags, param):
            nonlocal polygon
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(img, (x, y), 3, (0, 0, 127), -1)    
                if polygon: 
                    cv2.line(img, (polygon[-1][0], polygon[-1][1]), (x, y), (0, 0, 127), 2, cv2.LINE_AA)
                polygon.append([x,y])
            elif event == cv2.EVENT_RBUTTONDOWN:
                cv2.line(img, (polygon[-1][0], polygon[-1][1]), (polygon[0][0], polygon[0][1]), (0, 0, 127), 2, cv2.LINE_AA)
                list_polygon.append(polygon)
                polygon = []
        
        cv2.namedWindow(text)
        cv2.setMouseCallback(text,Draw_line)
        while(1):
            cv2.imshow(text,img)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
        return list_polygon
    def Create_remove_mask(self):
        self.polygon_remove = self.Draw_polygon(text = 'Select remove objects')
        self.mask_remove.fill(255)
        for each in self.polygon_remove:
            points = np.array(each)
            cv2.fillPoly(self.mask_remove, [points], (0))
        return 
    def Create_protect_mask(self):
        self.polygon_protect = self.Draw_polygon(text = 'Select protect objects')
        self.mask_protect.fill(255)
        for each in self.polygon_protect:
            points = np.array(each)
            cv2.fillPoly(self.mask_protect, [points], (0))
        return 
    def Delete_union(self):
        for each in self.polygon_remove:
            points = np.array(each)
            cv2.fillPoly(self.mask_protect, [points], (255))
        return  

    