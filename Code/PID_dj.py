#*************************************************************
#函数:  int16_t Idle_PID_Ctrl(setpoint , point) 
#功能:  增量式PID算法,得到增量值
#参数:  setpoint:    设定值
#       point:       当前值
#返回:  uk:          PID算法的控制增量
#描述:  返回增量值,即在上一次的控制量的基础上需要增加（负值意味减少）控制量
#**************************************************************/
def Idle_PID_Calc(setpoint,point): 
    if not hasattr(Idle_PID_Calc,'ek_2'):    #上上次误差
        Idle_PID_Calc.ek_2=0
    if not hasattr(Idle_PID_Calc,'ek_1'):    #上一次误差
        Idle_PID_Calc.ek_1=0
    if not hasattr(Idle_PID_Calc,'ek'):      #当前误差      
        Idle_PID_Calc.ek=0
    Kp = 0.15                  #Proportion
    Ki = 0.0                  #Integral
    Kd = 0.0                  #Differential    
                                                                      
    uk=0.0                      #控制量增量
                                        
    Idle_PID_Calc.ek = setpoint - point           #得到当前误差
    
    uk = int(Kp*(Idle_PID_Calc.ek - Idle_PID_Calc.ek_1)+ Ki*Idle_PID_Calc.ek + Kd*(Idle_PID_Calc.ek - 2*Idle_PID_Calc.ek_1 + Idle_PID_Calc.ek_2))  
   
    Idle_PID_Calc.ek_2 = Idle_PID_Calc.ek_1    
    Idle_PID_Calc.ek_1 = Idle_PID_Calc.ek     
   
    return (uk)   


def Idle_PID_Calc1(setpoint,point): 
    if not hasattr(Idle_PID_Calc,'Integral_error'):    #上上次误差
        Idle_PID_Calc.Integral_error=0
    if not hasattr(Idle_PID_Calc,'Last_error'):    #上一次误差
        Idle_PID_Calc.Last_error=0
    if not hasattr(Idle_PID_Calc,'uk'):    #结果
        Idle_PID_Calc.uk=0

    P = 0.15                  #Proportion
    I = 0.0                  #Integral
    D = 0.0                  #Differential 
      
    error = 0
    error = setpoint - point
    error = error

    Idle_PID_Calc.Integral_error += error
    
    Idle_PID_Calc.uk =(error*P+Idle_PID_Calc.Integral_error*I+(error-Idle_PID_Calc.Last_error)*D);

    track_PID.Last_error = error;

    return (Idle_PID_Calc.uk)


    