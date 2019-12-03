import React, { Component } from 'react';
import { Text, View, Image, Animated, Easing, StyleSheet, Button, Alert, ActivityIndicator } from 'react-native';
import {createSocket, send, listen, sendCancellingRequest, sendAndWaitWithTimeout} from './socketUtil.js'
import {acknowledgeMsg, getPreset} from './msgConstant';

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    height: '100%',
    backgroundColor: 'lightyellow',
  },
  titleContainer: {
    flex: 1,
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
    flex: 4, 
    alignContent: 'center', 
    justifyContent: 'center',
    flexDirection: 'row'
  },
  leaf: {
    alignSelf: 'center',
    width: 550,
    height: 550,
    resizeMode: 'contain',
    zIndex: 2,
    position: "absolute",
  },
  cancelModal: {
    height: '100%',
    width: '100%',
    position: "absolute",
    backgroundColor: 'lightyellow',
    top: 0,
    left: 0,
  }
})

class LoadScreen extends Component {
  constructor(props) {
    super(props)
    this.state = { 
      koala: new Animated.Value(0),
      koalaa: new Animated.Value(0),
      koalaaa: new Animated.Value(0),
      isCancelling: false,
    }
  }

  cancel() {
    this.setState({isCancelling: true})
    sendCancellingRequest()
    listen(() => {
      this.setState({isCancelling: false})
      sendAndWaitWithTimeout(getPreset(), (msgDecoded) => {
        const {replace} = this.props.navigation
        replace('Home', msgDecoded)
      }, 2)
    }, 13)
  }
  

  componentDidMount() {
    let self = this;
    Animated.loop(Animated.sequence([
      Animated.timing(
      this.state.koala, { 
        toValue: 1, 
        duration: 10, 
        easing: Easing.linear, 
        useNativeDriver: true, 
      }),
      Animated.delay(1000),
      Animated.timing(
        this.state.koalaa, { 
          toValue: 1, 
          duration: 10, 
          easing: Easing.linear, 
          useNativeDriver: true, 
        }),
      Animated.delay(1000),
      Animated.timing(
        this.state.koalaaa, { 
          toValue: 1, 
          duration: 10, 
          easing: Easing.linear, 
          useNativeDriver: true, 
        }),
        Animated.delay(1000),
        Animated.parallel([
          Animated.timing(
            this.state.koala, { 
              toValue: 0, 
              duration: 10, 
              easing: Easing.linear, 
              useNativeDriver: true, 
          }),
          Animated.timing(
            this.state.koalaa, { 
              toValue: 0, 
              duration: 10, 
              easing: Easing.linear, 
              useNativeDriver: true, 
          }),
          Animated.timing(
            this.state.koalaaa, { 
              toValue: 0, 
              duration: 10, 
              easing: Easing.linear, 
              useNativeDriver: true, 
          }),
          Animated.delay(1000),
        ]),
    ])).start();
    createSocket()
    if (this.props.navigation.state.params.isBrewing) {
      listen(() => {
         if (!this.state.isCancelling) {
          Alert.alert(
            'Brewing Finished',
            'Your tea is ready! Tea is best served while it is hot',
            [
              {text: 'Brew another tea', onPress: () => {
                send(acknowledgeMsg())
                sendAndWaitWithTimeout(getPreset(), (msgDecoded) => {
                  const {replace} = this.props.navigation
                  replace('Home', msgDecoded)
                }, 2)
              }},
              {text: 'Dismiss', onPress: () => {
                send(acknowledgeMsg())
              }},
            ]
          )
        };
      }, 4)
    } else {
      sendAndWaitWithTimeout(getPreset(), (msgDecoded) => {
        const {replace} = self.props.navigation
        replace('Home', msgDecoded)
      }, 2)
    }
  }

  render() {
    let titleText;
    let cancelButton;
    let cancelModal = this.state.isCancelling ? 
    <View style={styles.cancelModal}>
      <View style={styles.titleContainer}>
        <Text style={styles.titleText}>CANCELLING...</Text>
        <ActivityIndicator size="large" color="#00ff00" />
      </View>
    </View> : null
    if (this.props.navigation.state.params.isBrewing) {
      titleText = <Text style={styles.titleText}>Brewing</Text>;
      cancelButton = <Button title="Cancel" onPress={() => this.cancel()}/>
    } else {
      titleText = 
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
      cancelButton = null;
    }
    return (
      <View style={styles.mainContainer}>
        <View style={styles.titleContainer}>
          {titleText}
          {cancelButton}
        </View>
        <View style={styles.loaderContainer}>
        <Image style={styles.leaf} source={require('./assets/leaf.png')}></Image>
        <Animated.Image
          style={{width: 80, margin: 5, alignSelf: 'center', resizeMode: 'contain', opacity: this.state.koala }}
          source={require('./assets/koalaHead.png')} />
        <Animated.Image
          style={{width: 80, margin: 5, alignSelf: 'center', resizeMode: 'contain', opacity: this.state.koalaa }}
          source={require('./assets/koalaHead.png')} />
        <Animated.Image
          style={{width: 80, margin: 5, alignSelf: 'center', resizeMode: 'contain', opacity: this.state.koalaaa }}
          source={require('./assets/koalaHead.png')} />
        </View>
        {cancelModal}
      </View>
    );
  }
}

export { LoadScreen } 