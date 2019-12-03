import React, { Component } from 'react';
import { Text, View, StyleSheet, Picker, Button, ImageBackground } from 'react-native';
import {mockTeaProfile, mockAlarmArray} from './TestConstant.js';
import {send, listen, sendAndWaitWithTimeout} from './socketUtil.js';
import {removeTeaMsg, startBrewing} from './msgConstant';

const styles = StyleSheet.create({
    mainContainer: {
      flex: 1,
      height: '100%',
    },
    pickerContainer: {
      flex: 6,
      flexDirection: 'row'
    },
    pickerWrapper: {
      flex:1,
      margin: 2,
      borderWidth: 3,
      borderColor: 'green',
      borderRadius: 10,
      backgroundColor:'rgba(255,255,255,0.3)',
    },
    pickerHeader: {
      position:'absolute',
      top: 0,
      width: '100%',
      fontSize: 40,
      fontWeight: 'bold',
      textAlign: 'center',
      color: 'green',
    },
    picker: {
      marginTop: 100,
      height: 150, 
      width: '100%', 
      alignContent: 'center', 
      justifyContent: 'center',
    },
    InfoBox: {
      position: 'absolute',
      bottom: 0,
      height: 120, 
      width: '100%',
      fontSize: 15,
      textAlign: 'left',
    },
    InfoBox_zebra: {
      fontWeight: 'bold',
      textAlign: 'right',
    },
    deleteButtonContainer: {
      height: 50,
      width: '100%',
      position: 'absolute',
      bottom: 150,
      alignContent: 'center', 
      justifyContent: 'center',
    },
    buttonsContainer: {
      flex:1,
      flexDirection: 'row',
    },
    button: {
      flex: 1,
      margin: 'auto',
      alignContent: 'center', 
      justifyContent: 'center',
      borderColor: 'green',
      borderWidth: 3,
      borderRadius: 30,
      backgroundColor: 'white',
      margin: 20,
    },
})

class HomeScreen extends Component {
  state = {
    tea: mockTeaProfile[0].name,
    steepTime: mockTeaProfile[0].steepTime,
    temp: mockTeaProfile[0].temp,
    teaId: mockTeaProfile[0].teaId,
    isCustom: mockTeaProfile[0].isCustom,
    alarm: mockAlarmArray[0].name,
    alarmFileLocation: mockAlarmArray[0].fileLocation,
    teaProfileArray: mockTeaProfile,
    alarmArray: mockAlarmArray,
  }

  delete() {
    let tempTeaId = this.state.teaId
    sendAndWaitWithTimeout(removeTeaMsg(tempTeaId), () => {
      let filteredTeaProfile = this.state.teaProfileArray.filter((teaProfile) => {
        return teaProfile.teaId != tempTeaId
      })
      this.setState({ teaProfileArray: filteredTeaProfile})
    }, 10)
  }
  
  addTea(teaProfileArray) {
    const {navigate} = this.props.navigation
    navigate('AddTea', {'teas': teaProfileArray})
  }

  start() {
    sendAndWaitWithTimeout(startBrewing(
      this.state.tea,
      this.state.steepTime,
      this.state.temp,
      this.state.alarm,
      this.state.alarmFileLocation
    ), () => {
      const {replace} = this.props.navigation
      replace('Load', {'isBrewing': true, 'teas': this.state.teaProfileArray})
    }, 40)
  }

  componentDidMount() {
    if(this.props.navigation.state.params.teas) {
      let fetchedTeas = this.props.navigation.state.params.teas
      let fetchedAlarms = this.props.navigation.state.params.alarms
      this.setState({
        tea: fetchedTeas[0].name,
        steepTime: fetchedTeas[0].steepTime,
        temp: fetchedTeas[0].temp,
        teaId: fetchedTeas[0].teaId,
        isCustom: fetchedTeas[0].isCustom,
        alarm: fetchedAlarms[0].name,
        alarmFileLocation: fetchedAlarms[0].fileLocation,
        teaProfileArray: fetchedTeas,
        alarmArray: fetchedAlarms
      })
    }
  }

  render() {
    let teaProfileArray = this.state.teaProfileArray
    let teasPickerList = teaProfileArray.map(function(teaP, i){
      return <Picker.Item label={teaP.name} value={teaP.teaId} key={i} />
    }) 
    let alarmArray =  this.state.alarmArray
    let alarmsPickerList = alarmArray.map(function(alarm, i){
      return <Picker.Item label={alarm.name} value={alarm.name} key={i} />
    })
    
    return (
      <ImageBackground source={require('./assets/original.jpg')} style={{width: '100%', height: '100%'}}>
      <View style={styles.mainContainer}> 
        <View style={styles.pickerContainer}>
          <View style={styles.pickerWrapper}>
            <Text style={styles.pickerHeader}>
                TEA
            </Text>
            <Picker
                selectedValue={this.state.teaId}
                style={styles.picker}
                onValueChange={(itemValue, itemIndex) => {
                  this.setState({
                    tea: teaProfileArray[itemIndex].name,
                    steepTime: teaProfileArray[itemIndex].steepTime,
                    temp: teaProfileArray[itemIndex].temp,
                    teaId: itemValue,
                    isCustom: teaProfileArray[itemIndex].isCustom,
                  })
                }}
            >
                {teasPickerList}
            </Picker>
            <Text style={styles.InfoBox}>
              Name:
              <Text style={styles.InfoBox_zebra}>
              {`${this.state.tea}`}{"\n"}
              </Text>
              Steep Time:
              <Text style={styles.InfoBox_zebra}>
              {`${this.state.steepTime}`}ms{"\n"}
              </Text>
              Temperature:
              <Text style={styles.InfoBox_zebra}>
              {`${this.state.temp}`} &#8451;
              </Text>
            </Text>
            <View style={styles.deleteButtonContainer} >
              <Button
                title="Remove Tea"
                disabled={!this.state.isCustom}
                onPress={() => this.delete()}
              />
            </View>
          </View>
          <View style={styles.pickerWrapper}>
            <Text style={styles.pickerHeader}>
                ALARM
            </Text>
            <Picker
                selectedValue={this.state.alarm}
                style={styles.picker}
                onValueChange={(itemValue, itemIndex) =>
                    this.setState({
                      alarm: itemValue,
                      alarmFileLocation: alarmArray[itemIndex].fileLocation
                    })}
            >
                {alarmsPickerList}
            </Picker>
            <Text style={styles.InfoBox}>
              Name:
              <Text style={styles.InfoBox_zebra}>
              {`${this.state.alarm}`}
              </Text>
            </Text>
          </View>
        </View>
        <View style={styles.buttonsContainer}>
          <View style={styles.button}>
            <Button
              title="Add tea"
              onPress={() => this.addTea(teaProfileArray)}
            />
          </View>
          <View style={styles.button}>
            <Button
              title="Start"
              onPress={() => this.start()}
            />
          </View>
        </View>
      </View>
      </ImageBackground>
    );
  }
}

export {HomeScreen}