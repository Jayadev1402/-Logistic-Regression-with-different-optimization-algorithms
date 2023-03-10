import torchvision as thv
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
################################Training loop gradient descent
def train_gd(x, y,xx_val,y_val, L, lr,w):

  loss_arr = []
  for i in range(80):

    #gradient
    n = np.shape(x)[0]
    out=np.exp(-y*(w@x.T))
    num=(y*out).T
    den=(out+1).T
    nd=num /den
    grad = (-(1/n)*(x.T@nd)+L*w.T).T

    #Learning step
    w = w - lr*grad

    #Loss
    loss=np.sum(np.log(1 + out),axis=1)/np.shape(y)[0] + (L/2)*(np.linalg.norm(w)**2)
    loss_arr.append(loss[0])

  val_loss=0
  #gradient
  x=xx_val
  y=y_val
  n = np.shape(x)[0]
  out=np.exp(-y*(w@x.T))
  num=(y*out).T
  den=(out+1).T
  nd=num /den

  #Loss
  loss=np.sum(np.log(1 + out),axis=1)/np.shape(y)[0] 
  val_loss+=loss[0]

  return loss_arr,w,val_loss 

################################Training loop gradient descent with Nesterov
def train_nestrov(x, y, L, lr,w,r):
  u = np.random.rand(1,196)
  loss_arr = []
  for i in range(80):

    #gradient
    n = np.shape(x)[0]
    out=np.exp(-y*(w@x.T))
    num=(y*out).T
    den=(out+1).T
    nd=num /den
    grad = (-(1/n)*(x.T@nd)+L*w.T).T

    #Learning step
    u1=w-lr*grad
    w = u1*(1+r)-r*u
    u=u1
    #Loss
    loss=np.sum(np.log(1 + out),axis=1)/np.shape(y)[0] + (L/2)*(np.linalg.norm(w)**2)
    loss_arr.append(loss[0])

  return loss_arr,w 


################################Training loop SGD
def train_sgd(x_sgd, y_sgd, L, lr,w,batch):


  loss_arr = []
  for i in range(100):

    

    #Learning step
    batchh=np.random.randint(x_sgd.shape[0],size=batch)
    x=x_sgd[batchh]
    y=y_sgd[batchh]
    #gradient
    n = np.shape(x)[0]
    out=np.exp(-y*(w@x.T))
    num=(y*out).T
    den=(out+1).T
    nd=num /den
    grad = (-(1/n)*(x.T@nd)+L*w.T).T
    w = w - lr*grad

    #Loss
    loss=np.sum(np.log(1 + out),axis=1)/np.shape(y)[0] + (L/2)*(np.linalg.norm(w)**2)
    loss_arr.append(loss[0])
  return loss_arr,w 


################################Training loop SGD with Nesterov
def train_sgd_nesterov(x_sgd, y_sgd, L, lr,w,r,batch):

  u = np.random.rand(1,196)
  loss_arr = []
  for i in range(100):

    #Learning step
    batchh=np.random.randint(x_sgd.shape[0],size=batch)
    x=x_sgd[batchh]
    y=y_sgd[batchh]

    #gradient
    n = np.shape(x)[0]
    out=np.exp(-y*(w@x.T))
    num=(y*out).T
    den=(out+1).T
    nd=num /den
    grad = (-(1/n)*(x.T@nd)+L*w.T).T
    u1=w-lr*grad
    w = u1*(1+r)-r*u
    u=u1

    #Loss
    loss=np.sum(np.log(1 + out),axis=1)/np.shape(y)[0] + (L/2)*(np.linalg.norm(w)**2)
    loss_arr.append(loss[0])
  return loss_arr,w 





################################ Plot for GD
def plot_GD(xx_train,y_train,xx_val,y_val,w):
  s=[]
  L=[0.1,1,10,15,20,30,40,50] #Lambdas
  all_loss=[]
  val_loss_all=[]
  for i in range(len(L)):
    loss,_,val_loss = train_gd(xx_train, y_train,xx_val,y_val, L[i], 0.01,w)
    all_loss.append(loss)
    iter=range(len(all_loss[0]))
    slope, _ = np.polyfit(iter[:10], np.log(loss)[:10], 1) 
    s.append(slope)
    val_loss_all.append(val_loss)
    print(f'$\lambda$ : {L[i]}, slope : {slope},val_loss : {val_loss_all[i]}')

  # Semi-log plot
  for i in range(len(all_loss)):
    plt.semilogy(iter, all_loss[i],label=f"$\lambda$={L[i]}, slope={round(s[i],3)}, val_loss={round(val_loss_all[i],3)} ")
    
  plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
  plt.xlabel('No. of iterations')
  plt.ylabel('Training loss [log-scale]')
  plt.show()
  return s

################################ Plot for GD with nesterov
def plot_GD_nesterov(xx_train,y_train,w):
  r=[0.75,0.8,0.85,0.9,0.95] #Lambdas
  all_loss=[]
  val_loss_all=[]

  # lambda value obtained of slope from gradient descent
  l=10
  for i in range(len(r)):
    loss,_ = train_nestrov(xx_train, y_train, l, 0.01,w,r[i])
    all_loss.append(loss)
    iter=range(len(all_loss[0]))
  # Semi-log plot
  for i in range(len(all_loss)):
    plt.semilogy(iter, all_loss[i],label=f"ro={r[i]}")
  plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
  plt.xlabel('No. of iterations')
  plt.ylabel('Training loss [log-scale]')

  plt.show()

################################ Plot for SGD
def plot_SGD(xx_train,y_train,w):
  L=[10] #Lambdas
  all_loss=[]

  for i in range(len(L)):
    loss,_ = train_sgd(xx_train, y_train, L[i], 0.01,w,128)
    all_loss.append(loss)
    iter=range(len(all_loss[0])) 

  # Semi-log plot
  for i in range(len(all_loss)):
    plt.semilogy(iter, all_loss[i],label=f"$\lambda$={L[i]}")
  plt.legend()
  plt.xlabel('No. of iterations')
  plt.ylabel('Training loss [log-scale]')

  plt.show()

################################ Plot for SGD with nesterov
def plot_SGD_nesterov(xx_train,y_train,w):
  all_loss=[]

  l=10
  r=[0.8]
  for i in range(len(r)):
    loss,_ = train_sgd_nesterov(xx_train, y_train, l, 0.01,w,r[i],128)
    all_loss.append(loss)
    iter=range(len(all_loss[0])) 

  # Semi-log plot
  for i in range(len(all_loss)):
    plt.semilogy(iter, all_loss[i],label=f"ro={r[i]}")
  plt.legend()
  plt.xlabel('No. of iterations')
  plt.ylabel('Training loss [log-scale]')

  plt.show()
def plot_all(xx_train,y_train,xx_val,y_val,w):
  all_loss=[]
  l=10
  r=0.8
  lossGD,_,val_loss = train_gd(xx_train, y_train,xx_val,y_val, l, 0.01,w)
  lossSGD,_ = train_sgd(xx_train, y_train, l, 0.01,w,128)
  lossGDN,_ = train_nestrov(xx_train, y_train, l, 0.01,w,r)
  lossSGDN,_ = train_sgd_nesterov(xx_train, y_train, l, 0.01,w,r,128)

  plt.semilogy(range(len(lossGD)), lossGD,label=f"GD")
  plt.semilogy(range(len(lossSGD)), lossSGD,label=f"SGD")
  plt.semilogy(range(len(lossGDN)), lossGDN,label=f"GD-Nesterov")
  plt.semilogy(range(len(lossSGDN)), lossSGDN,label=f"SGD-Neseterov")
  plt.title('optimizers vs No. of iterations')
  plt.xlabel('No. of iterations')
  plt.ylabel('Training loss [log-scale]')
  plt.legend()

  plt.show()
def main():
  
  train = thv.datasets.MNIST('./', download=True, train=True)
  val = thv.datasets.MNIST('./', download=True, train=False)

  train = thv.datasets.MNIST('./', download=True, train=True)
  val = thv.datasets.MNIST('./', download=True, train=False)
  #Number of samples with 0 and 1 targets
  size_arr=np.where(train.targets==0)[0].shape[0]+np.where(train.targets==1)[0].shape[0]

  #Initializing 10000 samples for train and size_arr - 10000 samples for validation
  x_train=np.zeros([10000,28,28])
  y_train=np.zeros(10000)

  x_val=np.zeros([size_arr-10000,28,28])
  y_val=np.zeros(size_arr-10000)

  #Filling x_train, y_train and x_val, y_val
  z=0
  v=0
  for i in range(0,2):
    lst=np.where(train.targets==i)[0]

    idx1=lst[:5000]
    idx2=lst[5000:]

    x_train[z:5000+z]=train.data[idx1]
    y_train[z:5000+z]=train.targets[idx1]

    x_val[v:len(idx2)+v]=train.data[idx2]
    y_val[v:len(idx2)+v]=train.targets[idx2]

    z+=5000
    v+=len(idx2)

  #Creating list of numbers to be shuffled
  lst1=np.arange(0,10000)
  lst2=np.arange(0,size_arr-10000)

  #Shuffling train data
  random.shuffle(lst1)
  x_train=x_train[lst1]
  y_train=y_train[lst1]

  #Shuffling validation data
  random.shuffle(lst2)
  x_val=x_val[lst2]
  y_val=y_val[lst2]

  #Normalizing the pixel values
  x_train=x_train.reshape(-1,784)/255
  y_train=np.array(y_train)

  x_val=x_val.reshape(-1,784)/255
  y_val=np.array(y_val)

  #reshaping to 14x14
  xx_train=np.zeros((10000,196))
  xx_val=np.zeros((size_arr-10000,196))

  for i,val in enumerate(x_train):
      xx_train[i] = cv2.resize(x_train[i].reshape(28,28),(14,14)).flatten()

  for i,val in enumerate(x_val):
      xx_val[i] = cv2.resize(x_val[i].reshape(28,28),(14,14)).flatten()

  #Converting 0 to 1 and 1 to -1
  y_train[np.where(y_train==1)]=-1
  y_train[np.where(y_train==0)]=1

  y_val[np.where(y_val==1)]=-1
  y_val[np.where(y_val==0)]=1

  w = np.random.rand(1,196)
  slope=plot_GD(xx_train,y_train,xx_val,y_val,w)
  plot_GD_nesterov(xx_train,y_train,w)
  plot_SGD(xx_train,y_train,w)
  plot_SGD_nesterov(xx_train,y_train,w)
  plot_all(xx_train,y_train,xx_val,y_val,w)
if __name__=='__main__':
  main()
