import React, { Component } from "react";
import { createRoot } from 'react-dom/client';
//import { root } from 'ResultsPrinter';

// See https://stackoverflow.com/questions/39153545/how-to-do-post-in-form-submit-using-reactjs-and-pass-the-object-value-into-rest
class SubmitForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            placeholder: "Loading",
            query_seq: ""
        };
        this.onChange = this.onChange.bind(this); // See https://stackoverflow.com/questions/49931019/react-onchange-function-this-state-is-undefined
        this.executeQuery = this.executeQuery.bind(this); // See ^^
    }

    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }

    executeQuery(e) {
        e.preventDefault();

        fetch('api/query/', {
            method: 'POST',
            credentials: 'include', //See https://stackoverflow.com/questions/34558264/fetch-api-with-cookie ; https://web.dev/introduction-to-fetch/ ; https://testdriven.io/blog/django-spa-auth/
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'query_seq': this.state.query_seq })
        }).then(response => {
            if (response.status >= 400) {
                return this.setState(() => {
                    return { "query_seq": "Failed with HTTP status "+response.status+". Must enter a plain DNA sequence with only ACTGs. No FASTA format allowed."};
                });
            }
            else {
                this.setState({ "query_seq": 'Success! Submitted sequence to backend.' });
            }
        });



    }

    //See https://www.pluralsight.com/guides/how-to-use-multiline-text-area-in-reactjs for Textarea
    render() {
        return (
            <div className="SubmitForm">
                <form
                    id="dna-form"
                >
                    <label>
                        <textarea
                            id={"query_seq_area"}
                            name={"query_seq"}
                            value={this.state.query_seq}
                            rows={10}
                            cols={100}
                            placeholder={"DNA sequence goes here..."}
                            onChange={this.onChange}
                        />
                    </label>
                    <br />
                    <div className="align-left">
                        <button onClick={this.executeQuery}>Submit!</button>
                    </div>
                </form>
            </div>
        );
    }
}

SubmitForm.defaultProps = {
    action: '/api/query/',
    method: 'post'
};

export default SubmitForm;

const container = document.getElementById("post_form"); //Not sure why, but this has to be "app" to work on Chrome. On Safari & Firefox can be other things.
const root = createRoot(container);
root.render(<SubmitForm />, container);