require 'sys/proctable'

procs = Sys::ProcTable.ps()

save_log = true

log_file_path = File.join(File.expand_path('~/Desktop'), 'processes.log')
File.open(log_file_path, 'w') do |f|
  procs.each do |p|
    f.write("Process ID: #{p.pid}\n")
    f.write("Command line: #{p.cmdline}\n")
    f.write("Memory usage: #{p.rss} KB\n")
    f.write("Number of Threads: #{p.threads}\n")
    f.write("Author: #{p.euser}\n")
    ports = `lsof -i -P -n -p #{p.pid} | grep LISTEN | awk '{print $9}'`
    f.write("Port(s) used: #{ports}\n")

    f.write("---------------------\n")
    puts "Done"
  end
end

puts "Log file saved to #{log_file_path}"
