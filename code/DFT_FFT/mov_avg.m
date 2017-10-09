function y = mov_avg(d,y,y_type,t_type,type,time)
% Apply a moving average filter to signal y
    coeff = ones(1,d)/d;
    
    y = filter(coeff,1,y);
    
    figure
    plot(time,y)
    xlabel(t_type)
    ylabel(y_type)
    title([type,' ',y_type,' after moving average'])

end

