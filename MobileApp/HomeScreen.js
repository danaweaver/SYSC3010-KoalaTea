import React, { Component } from 'react';
import { Text, View, StyleSheet, Picker, Button } from 'react-native';
import {mockTeaProfile, mockAlarmArray} from './TestConstant.js';

const styles = StyleSheet.create({
    mainContainer: {
      flex: 1,
      height: '100%',
      backgroundColor: 'lightyellow',
    },
    pickerContainer: {
      flex: 5,
      flexDirection: 'row'
    },
    pickerWrapper: {
      flex:1,
      alignContent: 'center', 
      justifyContent: 'center',
      borderWidth: 1,
      borderColor: 'red',
    },
    picker: {
      height: 50, 
      width: 100, 
      flex: 2
    },
    pickerHeader: {
      flex: 2,
      alignContent: 'center', 
      justifyContent: 'center',
    },
    buttonsContainer: {
      flex: 1,
      flexDirection: 'row'
    }
})

class HomeScreen extends Component {
  state = {
    tea: '',
    alarm: '',
    steepTime: 0,
    temp: 0
  }
  render() {
    console.log(this.props.navigation);
    let teaProfileArray = this.props.navigation.state.params.teas ? this.props.navigation.state.params.teas : mockTeaProfile
    let teasPickerList = teaProfileArray.map(function(teaP, i){
      return <Picker.Item label={teaP.name} value={teaP.name} key={i} />
    }) 
    let alarmArray = this.props.navigation.state.params.alarms ? this.props.navigation.state.params.alarms : mockAlarmArray
    let alarmsPickerList = alarmArray.map(function(alarm, i){
      return <Picker.Item label={alarm.name} value={alarm.name} key={i} />
    }) 
    
    return (
      <View style={styles.mainContainer}> 
        <View style={styles.pickerContainer}>
          <View style={styles.pickerWrapper}>
            <Text style={styles.pickerHeader}>
                TEA
            </Text>
            <Picker
                selectedValue={this.state.tea}
                style={styles.picker}
                onValueChange={(itemValue, itemIndex) =>
                    this.setState({
                      tea: itemValue,
                      steepTime: teaProfileArray[itemIndex].steepTime,
                      temp: teaProfileArray[itemIndex].temp
                    })}
            >
                {teasPickerList}
            </Picker>
            <Text style={{flex: 2}}>{`
              Name:${this.state.tea}
              Steep Time:${this.state.steepTime}
              Temperature: ${this.state.temp}
              `}
            </Text>
          </View>
          <View style={styles.pickerWrapper}>
            <Text style={styles.pickerHeader}>
                ALARM
            </Text>
            <Picker
                selectedValue={this.state.alarm}
                style={styles.picker}
                onValueChange={(itemValue, itemIndex) =>
                    this.setState({alarm: itemValue})}
            >
                {alarmsPickerList}
            </Picker>
            <Text style={{flex: 2}}>{`
              Name:${this.state.alarm}
              `}
            </Text>
          </View>
        </View>
        <View style={styles.buttonsContainer}>
          <Button
            title="Add tea"
            onPress={() => {
              const {navigate} = this.props.navigation
              navigate('AddTea', {'teas': teaProfileArray})}
            }
          />
          <Button
          title="Start"
          onPress={() => Alert.alert('Simple Button pressed')}
        />
        </View>
      </View>
    );
  }
}

export {HomeScreen}