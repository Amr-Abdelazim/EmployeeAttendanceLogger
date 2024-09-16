from datetime import datetime, timedelta
class Employee:
    def __init__(self,id,name,department):
        self.id = id
        self.name = name
        self.department = department
        self.logs = dict()
    
    def add_log(self,date_str):
        date_obj = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
        date_only = date_obj.date()
        time_only = date_obj.time()
        if date_only in self.logs:
            if time_only <= self.logs[date_only][0]:
                self.logs[date_only][0] = time_only
            elif time_only >= self.logs[date_only][1]:
                self.logs[date_only][1] = time_only
        else:
            self.logs[date_only] = [time_only, time_only]

    def format_12h(self,time_only):
        # Create a new datetime object with a dummy date and the extracted time
        time_as_datetime = datetime.combine(datetime.min, time_only)

        # Format the time in 12-hour format with AM/PM
        time_12h = time_as_datetime.strftime("%I:%M %p")

        return time_12h

    def time_handle(self,time_log):# time_log = [first_time, last_time]
        if len(time_log) == 0:
            return ["NoFingerPrint", "NoFingerPrint", "NoFingerPrint"]
        dummy_date = datetime(2024, 1, 1)  # Any arbitrary date
        time0 = datetime.combine(dummy_date, time_log[0])
        time1 = datetime.combine(dummy_date, time_log[1])
        diff = time1 - time0
        hours = int(diff.total_seconds()//3600)
        minutes = int((diff.total_seconds() % 3600) // 60)
        
        check_in = self.format_12h(time_log[0])
        check_out = self.format_12h(time_log[1])

        total_work = f"{hours}:{minutes}"

        if hours < 4:# if employee worked more than 4 hour then no missing in (check_in, check_out)
            if time_log[0].hour >= 12:# if its pm so missing check_in
                check_in = "Missing"
                total_work = "Missing check_in"
            else:
                check_out = "Missing"
                total_work = "Missing check_out"
        
        
        return check_in, check_out, total_work



    def add_empty_days(self,first, last):# loop over all dayes form first to last and add not exists days
        date1 = datetime.strptime(first, "%m/%d/%Y")
        date2 = datetime.strptime(last, "%m/%d/%Y")
        while date1 <= date2:
            if date1.date() not in self.logs:
                self.logs[date1.date()] = []
            date1 += timedelta(days=1)

    def calc_late(self,worked_hour):
        total_work = 0
        worked_time = worked_hour.split(':')
        if len(worked_time) > 1:
            total_work += int(worked_time[0]) * 60 + int(worked_time[1])
        else:
            return 0

        late = max(8 * 60 - total_work, 0)
        if late <= 2 * 60:
            return late
        else:
            return 0

    def fetch_data(self, exceptions_dayes = [], exceptions_dates = []):
        data = []
        for key in sorted(self.logs):
            if key.strftime("%m/%d/%Y") in exceptions_dates:
                continue
            if key.strftime("%A") in exceptions_dayes:
                continue
            value = self.logs[key]
            check_in, check_out, worked_hours = self.time_handle(value)
            late = self.calc_late(worked_hours)
            late_str = f"{late // 60}:{late % 60}"
            data.append([self.id, self.name , self.department, key.strftime("%m/%d/%Y"), check_in, check_out, worked_hours, late_str])

        return data





        



