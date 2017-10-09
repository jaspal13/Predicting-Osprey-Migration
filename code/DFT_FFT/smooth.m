function y = smooth(d,y,y_type,t_type,type,time)
% smooth the signal by setting each latitude to be the average of its neighbours

for j = 1:d
    
    old = y;
    
    n = length(y);
    
    for i=1:n
        
        if i > 1 && i < n
            y(i) = (old(i-1)+old(i+1))/2;
            
        end
    end
end


figure
plot(time,y)
xlabel(t_type)
ylabel(y_type)
title([type,' ',y_type,' after smoothing'])


end

