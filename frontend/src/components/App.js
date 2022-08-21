import React, { Component } from "react";
import { render } from "react-dom";

// See https://blog.bitsrc.io/polling-in-react-using-the-useinterval-custom-hook-e2bcefda4197
// For details on the polling.

class App extends Component {
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
    fetch("api/lead") // https://www.smashingmagazine.com/2020/06/rest-api-react-fetch-axios/  https://www.freecodecamp.org/news/how-to-consume-rest-apis-in-react/
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
    fetch("api/lead") // https://www.smashingmagazine.com/2020/06/rest-api-react-fetch-axios/  https://www.freecodecamp.org/news/how-to-consume-rest-apis-in-react/
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
    return (
      <ul>
        {this.state.data.map(contact => {
          return (
            //This section is written in JSX - React's HTML-like DSL: https://reactjs.org/docs/introducing-jsx.html

            <li key={contact.id}>
              {contact.name} - {contact.email} - {contact.message}
            </li>

          );
        })}
        Polling count: {this.state.pollingCount}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("api_print_react_app"); //This seems to be what links this section into index.html
render(<App />, container);
