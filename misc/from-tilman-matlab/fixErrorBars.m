% By Tilman, help with making error bar plots look better
% ripped off from the Loren MATLAB blog
function fixErrorBars(handle, varargin)
    if (nargin == 1); w = 0.2; else w = varargin{1}; end
    hE_c                   = ...
            get(handle     , 'Children'    );
        errorbarXData          = ...
            get(hE_c(2), 'XData'       );
        errorbarXData(4:9:end) = ...
            errorbarXData(1:9:end) - w;
        errorbarXData(7:9:end) = ....
            errorbarXData(1:9:end) - w;
        errorbarXData(5:9:end) = ...
            errorbarXData(1:9:end) + w;
        errorbarXData(8:9:end) = ...
            errorbarXData(1:9:end) + w;
        set(hE_c(2), 'XData', errorbarXData);