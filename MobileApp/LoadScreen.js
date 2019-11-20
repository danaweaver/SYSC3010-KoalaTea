import React, { Component } from 'react';
import { Text, View, Image, Animated, Easing, StyleSheet } from 'react-native';
let dgram = require('react-native-udp');

const listeningPort = 3020;
const sendingPort = 3030; // default 3030
const sendingHost = 'localhost'; //'172.17.90.177'
const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    height: '100%',
    backgroundColor: 'lightyellow',
  },
  titleContainer: {
    flex: 3,
    alignContent: 'center', 
    justifyContent: 'center'
  },
  titleText: {
    color: 'green', 
    textAlign: 'center', 
    fontSize: 50, 
    fontWeight: 'bold'
  },
  lightgreen: {
    color: 'lightgreen'
  },
  loaderContainer: {
    flex: 2, 
    alignContent: 'center', 
    justifyContent: 'center'
  },
  koalaContainer: {
    flex: 4, 
    alignContent: 'center', 
    justifyContent: 'center'
  },
  koalaImg: {
    alignSelf: 'center', 
    width: 200, 
    height: 200
  }
})

function toByteArray(obj) {
  var uint = new Uint8Array(obj.length);
  for (var i = 0, l = obj.length; i < l; i++){
    uint[i] = obj.charCodeAt(i);
  }

  return new Uint8Array(uint);
}

function isEmpty(obj) {
  for(var key in obj) {
      if(obj.hasOwnProperty(key))
          return false;
  }
  return true;
}

class LoadScreen extends Component {

  state = { 
    spinValue: new Animated.Value(0),
    loading: true
  }

  componentDidMount() {
    let self = this;
    let socket = dgram.createSocket('udp4')
    Animated.loop(Animated.timing(
      this.state.spinValue, { 
        toValue: 1, 
        duration: 5000, 
        easing: Easing.linear, 
        useNativeDriver: true, 
      })).start();
    socket.once('listening', function() {
        let buf = toByteArray('{"msgId":2}')
        socket.send(buf, 0, buf.length, sendingPort, sendingHost, function(err) {
            if (err) throw err
            console.log('message was sent')
        })
    })
    socket.bind(listeningPort)
    socket.on('message', function(msg, rinfo) {
      console.log('message was received', msg)
      let msgDecoded = JSON.parse(String.fromCharCode.apply(null, new Uint8Array(msg)));
      if (!isEmpty(msgDecoded)) {
        console.log(123, msgDecoded);
        msgDecoded.socket = socket;
        self.setState({ loading : false})
        const {navigate} = self.props.navigation
        navigate('Home', msgDecoded)
      }
    })
  }

  render() {
    const spin = this.state.spinValue.interpolate({
      inputRange: [0, 1],
      outputRange: ['0deg', '360deg']
    })
    return (
      <View style={styles.mainContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>
            K
            <Text style={styles.lightgreen}>O</Text>
            A
            <Text style={styles.lightgreen}>L</Text>
            A
            <Text style={styles.lightgreen}>T</Text>
            E
            <Text style={styles.lightgreen}>A</Text>
          </Text>
        </View>
        <View style={styles.loaderContainer}>
        <Animated.Image
          style={{width: 150, alignSelf: 'center', height: 150, resizeMode: 'contain', transform: [{rotate: spin}] }}
          source={require('./assets/leaf.png')} />
        </View>
        <View style={styles.koalaContainer}>
          <Image style={styles.koalaImg} source={require('./assets/koala.png')}></Image>
        </View>
      </View>
    );
  }
}

export { LoadScreen } 