/* @flow weak */

import React, { Component } from 'react';

import moment from 'moment';

export default class GalleryImage extends Component {
  constructor(props) {
    super(props);

    let name = props.name;
    let date = name.substring(name.indexOf("_")+1, name.indexOf("."));
    name = name.substring(0, name.indexOf("_"));
    date = moment(parseInt(date + "000")).format("MMM Do, k:mm:ss")

    this.state = {
      date, name
    }
  }

  render() {
    const { name, date } = this.state;
    const { data } = this.props;
    return (
      <div className="gallery__image">
        <img className="gallery__image--image" src={data} alt=""/>
          <p className="gallery__image--date">{date}</p>
          <p className="gallery__image--name">{name}</p>
      </div>
    );
  }
}
