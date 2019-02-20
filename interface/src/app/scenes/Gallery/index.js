/* @flow weak */

import React, { Component } from 'react';
import { connect } from 'react-redux';

import Fetch from '../../util/Fetch';

import Navigator from '../Navigator';

import GalleryImage from '../../components/GalleryImage';

class Gallery extends Component {
  constructor(props) {
      super(props);

      this.state = {
        start: 0,
        images: [],
        imagedata: []
      }
  }

  componentWillMount() {}
  componentDidMount() {
    Fetch.images(this.state.start).then((res) => {
      this.setState({images: res.data.data}, () => {
        this.state.images.map((image) => {
          if(image[0] > 0) {
            Fetch.image(image[1]).then((res) => {
              let { imagedata } = this.state;
              imagedata.push({name: image[1], date: image[2], data: res.data.data});
              this.setState({imagedata});
            });
          }
        });
      });
    });
  }
  componentWillUnmount() {}

  renderFullImages() {
    const { imagedata } = this.state;

    return (
      <div className="gallery__imagecontainer">
        {imagedata.map((data, i) => {
          return <GalleryImage key={i} data={"data:image/png;base64," + data["data"]} name={data["name"]}/>
        })}
      </div>
    )
  }

  renderMobileImages() {

  }

  render() {
    const { imagedata } = this.state;
    return (
      <div className="gallery__container">
        <Navigator />
        {this.renderFullImages()}
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return { ...state };
}

export default connect(mapStateToProps)(Gallery);
