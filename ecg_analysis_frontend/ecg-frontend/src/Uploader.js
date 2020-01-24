import React from 'react'
import { post } from 'axios';

class SimpleReactFileUpload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file:null
        };
        this.state = {result : 'There will be result'};

        this.onFormSubmit = this.onFormSubmit.bind(this);
        this.onChange = this.onChange.bind(this);
        this.fileUpload = this.fileUpload.bind(this)
    }
    onFormSubmit(e){
        e.preventDefault(); // Stop form submit
        this.fileUpload(this.state.file)
            .then((response) => {
                this.setState({result : response.data});
                console.log(response)
            })
    }
    onChange(e) {
        this.setState({file:e.target.files[0]})
    }
    fileUpload(file){
        const url = 'http://localhost:8000/ecg/';
        const formData = new FormData();
        formData.append('files',file);
        const config = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        };
        return post(url,formData,config)
    }

    render() {
        return (
            <form onSubmit={this.onFormSubmit}>
                <h3>Upload file to get predictions</h3>
                <input type="file" onChange={this.onChange} />
                <button type="submit">Upload</button>
                <br/>
                <textarea value={this.state.result}></textarea>
            </form>
        )
    }
}

export default SimpleReactFileUpload