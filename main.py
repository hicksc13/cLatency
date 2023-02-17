import click
import datetime
import ping3
import os
import time
from pathlib import Path
from ezmail import send_email

EMAIL_THROTTLE = 5

##Email config 
#send_email(to_address, subject, body, attachments)

to_address = 'hicksc2013@gmail.com'
subject = 'Latency Report'
body = 'Inculded below are logs of when the latency was too high.'
attachments = None

@click.command()

def measure_latency():
    ans = click.confirm("Do you have a txt file to import?")
    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
        f.write(f"Welcome to the Latency test. Test Started at {current_time}\n")
        f.close()

    if ans:
        files = list(Path.cwd().glob("*.txt"))

        for i, file in enumerate(files):
            click.echo(f"{i + 1}. {file}")
        selected_file = files[click.prompt("Select the file you want to use", type=int) - 1]

        with open(selected_file, 'r') as f:
            ips = [line.replace('\n', '') for line in f.readlines()]
            threshold = click.prompt("Enter the latency threshold in milliseconds", default=100)
            interval = click.prompt("Enter the interval between pings in seconds", default=4)
            current_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")

    else:
        ips = [click.prompt("Enter the hostname or IP address to measure latency")]
        threshold = click.prompt("Enter the latency threshold in milliseconds", default=100)
        interval = click.prompt("Enter the interval between pings in seconds", default=4)

        current_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")

    last_email_time = datetime.datetime.now()

    while True:
        for ip in ips:
            try:
                latency = ping3.ping(ip, unit='ms')

                if latency == False:
                    click.echo("Ping failed host unknown 'cannot resolve'".format(ip))
                    with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                        f.write("{} {} {}ms host unknown 'cannot resolve'\n".format(current_time, ip, latency))

                if latency == None:
                    click.echo("Ping failed host timed out".format(ip))
                    with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                        f.write("{} {} {}ms timed out\n".format(current_time, ip, latency))

                if latency != False and latency != None and latency > threshold:
                    latency = round(latency, 2)
                    click.echo("Latency to {} is higher than threshold".format(ip))
                    with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                        f.write("{} {} {}ms\n".format(current_time, ip, latency))

                # Check if enough time has passed since last email
                elapsed_time = datetime.datetime.now() - last_email_time
                if elapsed_time.total_seconds() >= EMAIL_THROTTLE:
                    # Send email
                    attachments = "C:\\Users\\Owner\\Documents\\GitHub\\cLatency\\cLatency\\Latency_output.txt"
                    send_email(to_address, subject, body, attachments)
                    last_email_time = datetime.datetime.now()

                time.sleep(interval)
                print("Checking... Press Control+C to stop.")



            except Exception as e:
                click.echo("Error: {}".format(e))

        else:

            ips = [click.prompt("Enter the hostname or IP address to measure latency")]
            threshold = click.prompt("Enter the latency threshold in milliseconds", default=100)
            interval = click.prompt("Enter the interval between pings in seconds", default=4)

            
            current_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")

            while True:

                for ip in ips:
                    try:
                        latency = ping3.ping(ip, unit='ms')

                        if latency == False:
                            click.echo("Ping failed host unknown 'cannot resolve'".format(ip))
                            with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                                f.write("{} {} {}ms host unknown 'cannot resolve'\n".format(current_time, ip, latency))

                        if latency == None:
                            click.echo("Ping failed host timed out".format(ip))
                            with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                                f.write("{} {} {}ms timed out\n".format(current_time, ip, latency))

                        if latency > threshold:
                            latency = round(latency, 2)
                            click.echo("Latency to {} is higher than threshold".format(ip))
                            with open(os.path.expanduser("~/Desktop/Latency_output.txt"), "a") as f:
                                f.write("{} {} {}ms\n".format(current_time, ip, latency))



                        print("Checking... Press Control+C to stop.")
                        time.sleep(interval)

                    except Exception as e:
                        click.echo("Error: {}".format(e))



                
if __name__ == '__main__':

    measure_latency()