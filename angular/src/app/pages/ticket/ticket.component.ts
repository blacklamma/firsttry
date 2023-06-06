import { Component, OnInit } from '@angular/core';
import { TicketService } from './ticket.service';

@Component({
  selector: 'app-ticket',
  templateUrl: './ticket.component.html',
  styleUrls: ['./ticket.component.css']
})
export class TicketComponent implements OnInit {

  ticketData: any;
  page: number = 1;
  count: number = 0;
  tableSize: number = 25;
  constructor(private ticketService: TicketService) {}

  ngOnInit(): void{
    this.fetchTickets();
  }
  fetchTickets(): void {
    this.ticketService.getMyTickets().subscribe(
      (response) => {
        this.ticketData = response;
      }
    );
  }
  onTableDataChange(event: any) {
    this.page = event;
    this.fetchTickets();
  }
  onTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchTickets();
  }

}
