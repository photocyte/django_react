import React, { Component } from "react";
import { createRoot } from 'react-dom/client';
//const crypto = import('node:crypto');

// See https://blog.bitsrc.io/polling-in-react-using-the-useinterval-custom-hook-e2bcefda4197
// For details on the polling.

class ResultsPrinter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
      pollingCount: 0,
      delay: 1000
    };
  }

  componentDidMount() {
    this.interval = setInterval(this.tick, this.state.delay);
    fetch("api/query/") // https://www.smashingmagazine.com/2020/06/rest-api-react-fetch-axios/  https://www.freecodecamp.org/news/how-to-consume-rest-apis-in-react/
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }


  componentDidUpdate(prepProvs, prevState) {
    if (prevState.delay != this.state.delay) {
      clearInterval(this.interval);
      this.internval = setInterval(this.tick, this.state.delay);
    }

  }



  tick = () => {
    this.setState({
      pollingCount: this.state.pollingCount + 1
    });
    //Refetch the data from the API, each time the tick changes.
    fetch("api/query/") // https://www.smashingmagazine.com/2020/06/rest-api-react-fetch-axios/  https://www.freecodecamp.org/news/how-to-consume-rest-apis-in-react/
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }



  render() {
    var tableStyle = {
      "width": "1050px",
      "border": "1px solid black",
      "borderCollapse": "collapse"
    };
    var colStyle1 = {
      "width": "200px",
      "textAlign": "center",
      "border": "1px solid black",
      "borderCollapse": "collapse"
    };
    var colStyle2 = {
      "width": "650px",
      "border": "1px solid black",
      "borderCollapse": "collapse"
    };

    return (
      <table className="pure-table-odd" style={tableStyle}>
        
        <thead><tr><th style={colStyle1}>Input Seq</th><th style={colStyle1}>Status</th><th style={colStyle2}>Results (raw <a href="https://github.com/bbuchfink/diamond/wiki/3.-Command-line-options#output-options">--outfmt 6</a> <a href="https://github.com/bbuchfink/diamond">Diamond</a> output)</th></tr></thead>
        <tbody>
        {this.state.data.map(row => {
          return (
            //This section is written in JSX - React's HTML-like DSL: https://reactjs.org/docs/introducing-jsx.html

            <tr key={row.id}>
              <td style={colStyle1}>Input seq with length: {row.query_seq.length}</td><td style={colStyle1}>{row.alignment_status}</td><td style={colStyle2}>{row.results}</td>
            </tr>
          );
        })}
        </tbody>
      </table>
      //Polling count: {this.state.pollingCount}
    );
  }
}


export default ResultsPrinter;

const container = document.getElementById("app"); //Not sure why, but this has to be "app" to work on Chrome. On Safari & Firefox can be other things.
const root = createRoot(container);
root.render(<ResultsPrinter />, container);
