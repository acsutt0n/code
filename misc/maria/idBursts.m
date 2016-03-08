%
%
%
%

function bursttms = idBursts(paths, dT)

if nargin < 2
  dT = 0.0001;
else
  dT = dT;
end

bursttms = {};

for fn = 1:length(paths)
  % Load the trace
  trace = abfload(paths{fn});
  trace = trace(:,1);
  % Display the trace for manual burst targeting
  plot(dT:dT:length(trace)*dT, trace);
  title('Identify BURSTS! Press Enter to stop.');
  [x,y] = ginput(200);
  
  % Identify and record the burst windows
  tfil = strsplit(paths{fn}, '.');
  try
    tfil = char(tfil(end-1));
  catch
    tfil = char(paths{fn});
  end
  tfil = ['id_', tfil];
  % fprintf('%s', tfil);
  durs = [];
  for i = 1:length(x)/2
    durs = [durs; x(i*2-1), x(i*2)];
  bursttms = setfield(bursttms, tfil, durs);
end


  






























end