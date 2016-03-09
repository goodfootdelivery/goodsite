<?php

/*

Template Name: Place an Order Beta

*/

//

//ini_set( 'display_errors', 1 );
//ini_set( 'scream.enabled', 1 );		// >= v.5.2.0
//error_reporting( E_ALL ^ E_NOTICE );
//error_reporting( E_ALL );

//check to make sure logged in or admin, otherwise DIE
if ( !is_user_logged_in()  ) {
echo "You need to <a href=\"http://www.goodfootdelivery.com\">log-in</a> to view this page";
 echo do_shortcode('[sp_login_shortcode]');
die();
}

//check to make sure a form has been submitted, otherwise DIE
if (empty($_POST) ){
echo 'You need to start <a href="http://www.goodfootdelivery.com/start-place-order">here</a>';
die;	
}

require_once( '/home8/goodfop0/public_html/track/general-functions.php' );  //geocoding, distance measurements, pricing(NTD)


class Wp_Layout_Template extends Wp_Layout {

	private $oUser;
	private $aAddrDelivery;
	private $aAddrPickup;
	//
	public function init( $bUnshift = FALSE ) {
		parent::init( $bUnshift );
		$this->oUser = $this->newMember();
		if ( $this->oUser->getId() ) {
			$aAddresses = $this->newMember_Address_Query( array(
				'object_id' => $this->oUser->getId(),
				'showposts' => -1
			), FALSE );

			$aAddrTypes = Geko_Wp_Enumeration_Query::getSet( 'user-address-type' );
			$this->aAddrDelivery = $aAddresses->subsetAddressTypeId( $aAddrTypes->getValueFromSlug( 'delivery' ) );
			$this->aAddrPickup = $aAddresses->subsetAddressTypeId( $aAddrTypes->getValueFromSlug( 'pick-up' ) );
		}
		return $this;
	}
	//
	public function echoEnqueue() {
		wp_enqueue_script( 'geko-jquery-json' );
		wp_enqueue_script( 'geko-jquery-form' );
		wp_enqueue_script( 'geko-jquery-ui-datepicker' );
		wp_enqueue_style( 'geko-jquery-ui-wp' );
	}
	//
	public function echoHeadLate() {
		$aJsonParams = array(
			'script' => array(
				'url' => get_bloginfo( 'url' ),
				'process' => get_bloginfo( 'template_directory' ) . '/services/process.php',
				'wp_login' => get_bloginfo( 'url' ) . '/wp-login.php'
			),
			'status' => array(
				'login_success' => Geko_Wp_Login::STAT_LOGIN_SUCCESS,
				'order_processed' => Wp_Service_ProcessOrder::STAT_ORDER_PROCESSED,
				'new_user' => Wp_Service_ProcessOrder::STAT_NEW_USER,
				'user_exists' => Wp_Service_ProcessOrder::STAT_USER_EXISTS,
				'register' => Wp_Service_ProcessOrder::STAT_REGISTER
			),
			'year' => date( 'Y' ),
			'is_logged_in' => ( ( $this->oUser->getId() ) ? TRUE : FALSE ),
			'show_login_form' => ( ( $_GET[ 'login' ] ) ? TRUE : FALSE ),
			'has_addr_delivery' => ( ( ( $this->aAddrDelivery ) && ( $this->aAddrDelivery->count() > 0 ) ) ? TRUE : FALSE ),
			'has_addr_pickup' => ( ( ( $this->aAddrPickup ) && ( $this->aAddrPickup->count() > 0 ) ) ? TRUE : FALSE )
		);
		
		?>
		<link rel="stylesheet" type="text/css" href="<?php bloginfo( 'template_directory' ); ?>/styles/order_form.css" media="screen" />
		<link rel="stylesheet" type="text/css" href="<?php bloginfo( 'template_directory' ); ?>/styles/temp_style.css" media="screen" />
		
    	<script type="text/javascript">
			jQuery( document ).ready( function( $ ) {
				var borderDefinition = 'solid 2px #f00';
				var oParams = <?php echo Zend_Json::encode( $aJsonParams ); ?>;
				//

				$('#express').click(function() {
						$('input:radio[name=service-level]').val(['express']);
				});

				$('#basic').click(function() {
						$('input:radio[name=service-level]').val(['basic']);
				});

				$('#orderSubmit').click(function() {
						$('form#submitOrder').submit();
				});
				


				var fSetUserStatus = function( data ) {

					

					// dynamically set the user status section

					$( '#container div.user_status' ).html(

						'<ul>' + 

							'<li><strong>Logged in as:<\/strong> ' + data.full_name + '<\/li>' + 

							'<li class="loginButton"><a href="' + oParams.script.url + '/address-book/">Address Book<\/a><\/li>' + 

							'<li class="loginButton"><a href="' + oParams.script.url + '/order-history/">Order History<\/a><\/li>' + 

							'<li class="loginButton"><a href="' + oParams.script.url + '/account-info/">Account Info<\/a><\/li>' + 

							'<li class="loginButton"><a href="' + data.logout_url + '" test="' + data.test + '">Log-out<\/a><\/li>' + 

						'<\/ul>'

					);

					

				}

				

				////

				

				$( '#date' ).datepicker( {
					changeMonth: true,
					changeYear: false,

					changeMonth: true,
					changeYear: false,
				} );

	

				//// toggles

				

				$( '#useFromManual' ).click( function() {

					$( '#manualSectionFrom' ).show( 300 );

					$( '#addrBookSectionFrom' ).hide( 300 );

				} );

				

				$( '#useFromAddrBook' ).click( function() {

					$( '#manualSectionFrom' ).hide( 300 );

					$( '#addrBookSectionFrom' ).show( 300 );

				} );

				

				$( '#useToManual' ).click( function() {

					$( '#manualSectionTo' ).show( 300 );

					$( '#addrBookSectionTo' ).hide( 300 );				

				} );

				

				$( '#useToAddrBook' ).click( function() {

					$( '#manualSectionTo' ).hide( 300 );

					$( '#addrBookSectionTo' ).show( 300 );				

				} );

				

				//// init

				

				$( '#orderConfirmation, #formErrors, #register_section, #login_section, .ajax_loading, #addrBookSectionTo, #addrBookSectionFrom, #print_waybill' ).hide();


				if ( !oParams.has_addr_pickup ) $( '#toggleFrom' ).hide();
				if ( !oParams.has_addr_delivery ) $( '#toggleTo' ).hide();
				if ( oParams.show_login_form ) $( '#botLoginMain' ).click();
			} );
		</script>
    	<?php	
	}
	//
		public function echoContent() {
			
						$db = new mysqli('localhost', 'goodfop0_gfgd', 'r5P4hSfhb8', 'goodfop0_deliverydb');
						if($db->connect_errno > 0){
						die('Unable to connect to database [' . $db->connect_error . ']');
					}
			
		$GKEY = "AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok";	
		$GKEY2= "AIzaSyB4eIwGagrhq24UcXEuY6_--DF1J5aDX1g";
			
		$aServiceLevels = Geko_Wp_Enumeration_Query::getSet( 'user-order-service-level' );
		$oLocation = Wp_Member_Location_Manage::getInstance()->init();
		
		//get posted variables from first order form
		$pu_address = $_POST['pick-up-address'];  //this is what ultimately gets geocoded
		$pu_unit = $_POST['pick-up-unit'];
		$pu_care_of = $_POST['pick-up-care-of'];
		$pu_phone = $_POST['pick-up-phone'];
			
		$do_address = $_POST['drop-off-address'];  //this is what ultimately gets geocoded
		$do_unit = $_POST['drop-off-unit'];
		$do_care_of = $_POST['drop-off-care-of'];
		$do_phone = $_POST['drop-off-phone'];
	
		$comments = $_POST['comments'];
		
		$pu_address_book_toggle = $_POST['useFrom'];
		$do_address_book_toggle = $_POST['useTo'];		
		
		$pu_address_book_id = $_POST['addrBookIdFrom'];
		$do_address_book_id = $_POST['addrBookIdTo'];
		

		// build the pickup information

				if ($pu_address_book_toggle == 'addr_book'){  //address book entry, get specific address info from the DB (i.e. unit and contact)

					$sql = "SELECT * FROM wp_geko_location_address WHERE object_id = $pu_address_book_id";
					$result = $db->query($sql);
					$row = $result->fetch_assoc();
					$pu_care_of = $row['address_line_1'];
					$pu_address = $row['address_line_2'];
					//$pu_city = $row['city'];
					$pu_city = 'Toronto';  //hack to make address book entries work (Toronto ONLY)
					$pu_address = "$pu_address, $pu_city";
					$pu_unit = $row['address_line_3'];
					
				}
				
				$pucoord = geocode($pu_address);  //geocode pickup
				$pu_lat = $pucoord['0'];
				$pu_lng = $pucoord['1'];
				$pu_coords = array ( $pucoord['0'], $pucoord['1'] ) ;
				$pu_street_number = $pucoord['2'];	
				$pu_street_name = $pucoord['3'];
				$pu_city = $pucoord['4'];
				$pu_province = $pucoord['5'];
				$pu_postal_code = $pucoord['6'];
				//$pu_country = $_POST['pu_country'];
				$pickup = "$pu_street_number $pu_street_name, $pu_city $pu_province. $pu_postal_code";
				$pu_address = "$pu_street_number $pu_street_name";

				//build the drop off information 
			
				if($do_address_book_toggle == 'addr_book'){ //address book entry, get extra address info from the DB (i.e. unit and contact info)

				$sql = "SELECT * FROM wp_geko_location_address WHERE object_id = $do_address_book_id";
				$result = $db->query($sql);
				$row = $result->fetch_assoc();
				$do_care_of = $row['address_line_1'];
				$do_address = $row['address_line_2'];
				//$do_city = $row['city'];
				$do_city = 'Toronto';
				$do_address = "$do_address, $do_city";
				$do_name = $row['address_line_1'];
				$do_unit = $row['address_line_3'];
				
				}

			$docoord = geocode($do_address);
			$do_lat = $docoord['0'];
			$do_lng = $docoord['1'];
			$do_coords = array ( $docoord['0'], $docoord['1'] ) ;
			$do_street_number = $docoord['2'];	
			$do_street_name = $docoord['3'];
			$do_city = $docoord['4'];
			$do_province = $docoord['5'];
			$do_postal_code = $docoord['6'];
			//$do_country = $_POST['do_country'];
			$dropoff = "$do_street_number $do_street_name, $do_city $do_province. $do_postal_code";
			$do_address = "$do_street_number $do_street_name";
			
			$ready_date = $_POST['ready-date'];
			$next_date = date('m/d/Y', strtotime($ready_date . ' +1 day'));
			if ((date('N', strtotime($next_date)) >= 6)){
				$weekend = 'true';
				$next_date = date('m/d/Y', strtotime($next_date . ' next Monday'));  //push next day to Monday if it falls on a weekend
			}
			
			
	//	$readyTimeHours = $_POST['readyTimeHours'];
	//	$readyTimeMinutes = $_POST['readyTimeMinutes'];
	//	$timeSelect = $_POST['timeSelect'];
	//	$time = $readyTimeHours . ":" . $readyTimeMinutes . " " . $timeSelect;
		$ready_time = $_POST['time-select'];
		$clean_ready_time  = date("H:i", strtotime("$ready_time"));
		$string_ready_time = strtotime($clean_ready_time);
		$envelope = $_POST['qtdEnvelopes'];
		$boxorbag = $_POST['qtdBoxorBag'];
		$other = $_POST['qtdOther'];
	
		if($envelope != ''){ $package_type = 'Envelope: ' . $envelope; }
		if($boxorbag != ''){ $package_type = 'Box or Bag: ' . $boxorbag; }
		if($other != ''){ $package_type = 'Other: ' . $other; }

// generate prices and service levels
	$url2 = 'https://maps.googleapis.com/maps/api/directions/json?'.
	'origin='.				"$pu_lat,$pu_lng".
	'&destinations='.		"$do_lat,$do_lng".
	'&departure_time='.		"$string_ready_time".
	'&mode=transit'.
	'&transit_mode=subway'.
	'&transit_preference=LESS_WALKING'.
	'&key='.		"$GKEY2";
	

	$url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='.
		"$pu_lat,$pu_lng".
		'&destinations='.
		"$do_lat,$do_lng".
		'&departure_time='.
		"$string_ready_time".
		'&traffic_model=best_guess'.
		'&mode=transit'.
		'&key='."$GKEY";


    // get the json response
	$resp_json = file_get_contents($url);
	//echo $resp_json;

	$resp = json_decode($resp_json, true);
 
    // response status will be 'OK', if able to geocode given address
    if($resp['status']='OK'){
 
        // get the important data
		
		$timevalue = $resp['rows'][0]['elements'][0]['duration']['value'];
       
        // verify if data is complete
        if($timevalue){
			$hours = $timevalue / 3600;
		
			//CALCULATE PRICE & SERVICE LEVELS
			
			
			// START CONFIG
			
			$hourly_rate = "16";  // hourly rate for deliveries
			$express_premium = "1.7";  //express price multiplier
			$basic_cut_off_time = "14:00:00"; //same day cut-off
			$express_cut_off_time = "16:00:00"; //same day cut-off
			$long_distance_cut_off_time = "12:00:00"; //long distance cut-off
			$long_distance_trigger = '1.1'; // Number of hours in transit before delivery becomes expanded zone
			$long_distance_premium = "1.1"; // long distance price multiplier
			
			$office_opening_time = "09:00:00";
			
			$minimum_basic = "8.50";  // minimum basic charge
			$minimum_express = "15.00";   // minimum express charge
			$minimum_long_distance = "22.50";
			
			$maximum_basic = "60";  // maximum basic charge
			$maximum_express = "80";   // maximum express charge
			$maximum_long_distance = "80";
			

			// END CONFIG
			$string_basic_cut_off_time = strtotime($basic_cut_off_time);
			$string_express_cut_off_time = strtotime($express_cut_off_time);
			$string_long_distance_cut_off_time = strtotime($long_distance_cut_off_time);
			$string_office_opening_time = strtotime($office_opening_time);
			
			// check for long distance (more than 1:00 transit)
			if($hours > $long_distance_trigger){
				$long_distance_price = round($hours * $hourly_rate * $long_distance_premium * 2, 0)/2;
				$long_distance_price = number_format($long_distance_price, 2, '.', ',');
			
				if($string_ready_time >= $string_long_distance_cut_off_time || $weekend == 'true' ){ // if true, the pickup is after the same day cutoff for basic
				$long_distance_guarantee = "Deliver by: " . $next_date . " @ 5:00PM";
				}
				else {
				
				$long_distance_guarantee = "Deliver by: " . $ready_date . " @ 5:00PM";	
				}
				
			}
			
			else {
			
			$basic_price = round($hours * $hourly_rate * 2, 0)/2;
			$basic_price = number_format($basic_price, 2, '.', ',');
				if ($basic_price <= $minimum_basic){ 
			$basic_price = $minimum_basic; 
				}
			
			$express_price = round($hours * $hourly_rate * $express_premium * 2, 0)/2;
				$express_price = number_format($express_price, 2, '.', ',');
				if ($express_price <= $minimum_express){ 
				$express_price = $minimum_express; 
				}
			
				if($string_ready_time >= $string_basic_cut_off_time || $weekend == 'true' ){ // if true, the pickup is after the same day cutoff for basic
				$basic_guarantee = "Deliver by: " . $next_date . " @ 5:00PM";
				}
			
				else {
				
				$basic_guarantee = "Deliver by: " . $ready_date . " @ 5:00PM";
				}
			
				if($string_ready_time >= $string_express_cut_off_time || $weekend == 'true' ){ // if true, the pickup is after 4pm and before 9AMso deliver next day by noon
				$express_guarantee = "Deliver by: " . $next_date . " @ 12 Noon";
				}
	
				else {
				$express_guarantee = "Deliver in 2.5 hours or less.";
				}
			}
			
        }else{
            $failure = 'Failed to get a time value';
			
        }
         
    }else{
		   $failure = 'Failed to get OK API call';
    }


		?>

        <div id="submitOrder">
		<form id="submitOrder"  action="/order-placed" method="post">
		<?

		?>
		<div id="order_section">
		
		<? if ($express_price && $basic_price){ 
		echo "<input type='hidden' name='basic-price' value='$basic_price'>";
		echo "<input type='hidden' name='basic-guarantee' value='$basic_guarantee'>";
		echo "<input type='hidden' name='express-price' value='$express_price'>";
		echo "<input type='hidden' name='express-guarantee' value='$express_guarantee'>";
		?>
		<table id="tableOrder" width="687">
				<tr><td>
					<p></p>
							<h2>Price & Service Level</h2>
							<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_full.gif" />
					<p></p>
					</td></tr>
					<tr>
					<td>
					
				<div id="express" class="need-input" style="border-color:green; border-width:3px; background-color:#99CC66;">
					<input type="radio" name="service-level" value="express">
					<span class="service-label">Express<span style="font-size:14px;">&nbsp;<? echo $express_guarantee; ?></span></span>
					<span class="price-style">$<?echo $express_price?></span>
					</div>			
					

	   <p></p>
	   	<div id="basic" class="need-input" name="service-level" value="basic" style="border-color:grey; border-width:3px; background-color:#D3D3D3;">			
			<input type="radio" name="service-level" value="basic" checked="checked">
					<span class="service-label">Basic<span style="font-size:14px;">&nbsp;<? echo $basic_guarantee; ?></span></span>
					<span class="price-style">$<?echo $basic_price?></span>
					</div>		
		</td></tr>
		</table>
		
		<? } else { 
		echo "<input type='hidden' name='long-distance-price' value='$long_distance_price'>";
		echo "<input type='hidden' name='long-distance-guarantee' value='$long_distance_guarantee'>";
		?>
			

	<table id="tableOrder" width="687">
			<tr>
				<td>
				<p></p>
					<h2>Price & Service Level</h2>
						<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_full.gif" />
					<p></p>
				</td>
			</tr>
			<tr>
				<td>
					<div class="need-input" style="border-color:green; border-width:3px; background-color:grey;">
					<input type="radio" name="service-level" value="long-distance" checked="checked">
					<span class="service-label">Basic<span style="font-size:14px;">&nbsp;<? echo $long_distance_guarantee; ?></span></span>
					<span class="price-style">$<?echo $long_distance_price?></span>
					</div>
				</td>
			</tr>
	</table>
		
		<? } ?>
		
		
		<table id="tableOrder" width="687">
			<tr>
				<td width="332" valign="top">
					<p></p>
							<h2>Pick Up </h2>
										<? 
											echo "<input type='hidden' name='pick-up-address' value='$pu_address'>";
											echo "<input type='hidden' name='pick-up-unit' value='$pu_unit'>";
											echo "<input type='hidden' name='pick-up-city' value='$pu_city'>";
											echo "<input type='hidden' name='pick-up-province' value='$pu_province'>";
											echo "<input type='hidden' name='pick-up-postal' value='$pu_postal_code'>";
											echo "<input type='hidden' name='pick-up-lat' value='$pu_lat'>";
											echo "<input type='hidden' name='pick-up-lng' value='$pu_lng'>";
											echo "<input type='hidden' name='pick-up-care-of' value='$pu_care_of'>";
											echo "<input type='hidden' name='pick-up-phone' value='$pu_phone'>";
										?>
								<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
								<p>
								<img width="100%" src="http://maps.googleapis.com/maps/api/staticmap?center=<? echo "$pu_lat,$pu_lng"; ?>&zoom=14&scale=false&size=300x150&maptype=roadmap&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:1%7C<? echo "$pu_lat,$pu_lng"; ?>&markers=size:mid%7Ccolor:0xff0000%7Clabel:1%7C<? echo "$pu_lat,$pu_lng"; ?>">
								</p>
								<div id="manualSectionFrom">
									<table class="formLine" width="100%">
											<tr>
												<td><label>Address</label></td>
												<td width="100%">
													<label style="color:grey;">
													<? echo "$pickup"; 
													if ($pu_unit != ''){ echo "&nbsp;<label style='color:black;'> Unit</label>$pu_unit"; } 
													?>
													</label>
												</td>
											</tr>
									</table>
		

		
										<table class="formLine" width="100%">
											<tr >
												<td nowrap><label>Care of </label></td>
												<td width="100%">
													<label style="color:grey;"><? echo "$pu_care_of"; ?></label>
												</td>
											</tr>
										</table>
						
												<table class="formLine" width="100%">
											<td><label>Phone</label></td>
												<td width="100%">
													<label style="color:grey;"><? echo "$pu_phone";?></label>
												</td>
											</table>
										
										<?  $pu_address_book_toggle; if ($pu_address_book_toggle == 'manual'){ ?>
										<table class="formLine" width="100%">
											<tr>
												<td nowrap><label>Save To Address Book?</label></td>
												<td width="100%"> <input type="checkbox" name="pick-up-save" value="1" />
												</td>
											</tr>
										</table>
										<? } ?>

								</div>
								
							</td>
							<td width="23">&nbsp;</td>
							<td width="332" valign="top">
								
<p></p>
								<h2>Drop-off </h2>
								
								<? 
										
											echo "<input type='hidden' name='drop-off-address' value='$do_address'>";
											echo "<input type='hidden' name='drop-off-unit' value='$do_unit'>";
											echo "<input type='hidden' name='drop-off-city' value='$do_city'>";
											echo "<input type='hidden' name='drop-off-province' value='$do_province'>";
											echo "<input type='hidden' name='drop-off-postal' value='$do_postal_code'>";
											echo "<input type='hidden' name='drop-off-lat' value='$do_lat'>";
											echo "<input type='hidden' name='drop-off-lng' value='$do_lng'>";
											echo "<input type='hidden' name='drop-off-care-of' value='$do_care_of'>";
											echo "<input type='hidden' name='drop-off-phone' value='$do_phone'>";
								?>
							
							
								<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
<p>
								<img width="100%" src="http://maps.googleapis.com/maps/api/staticmap?center=<? echo "$do_lat,$do_lng"; ?>&zoom=14&scale=false&size=300x150&maptype=roadmap&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:1%7C<? echo "$do_lat,$do_lng"; ?>&markers=size:mid%7Ccolor:0xff0000%7Clabel:1%7C<? echo "$do_lat,$do_lng"; ?>">
</p>
							
				
								<div id="manualSectionTo">
								

								
								<table class="formLine" width="100%">
											<tr>
												<td><label>Address</label></td>
												<td width="100%">
													<label style="color:grey;">
													<? echo "$dropoff"; 
													if ($pu_unit != ''){ echo "&nbsp;<label style='color:black;'> Unit</label>$do_unit"; } 
													?>
													</label>
												</td>
											</tr>
									</table>
		

		
										<table class="formLine" width="100%">
											<tr>
												<td nowrap><label>Care of </label></td>
												<td width="100%">
													<label style="color:grey;"><? echo "$do_care_of"; ?></label>
												</td>
											</tr>
										</table>
						
										<table class="formLine" width="100%">
											<td><label>Phone</label></td>
												<td width="100%">
													<label style="color:grey;"><? echo "$do_phone";?></label>
												</td>
										</table>
											<? if ($do_address_book_toggle == 'manual'){ ?>
										<table class="formLine" width="100%">
											<tr>
												<td nowrap><label>Save To Address Book?</label></td>
												<td width="100%"> <input type="checkbox" name="drop-off-save" value="1" />
												</td>
											</tr>
										</table>
											<? }?>
											
											
								
								
								</div>
								
								
							</td>
						</tr>
					</table>
					<table id="tableOrder" width="687">
							<tr>
							<td width="332" valign="top">
							
							<p></p>
							<h2>Details</h2>
									<?php 
											
											//$time  = date("H:i", strtotime("$readyTimeHours . ":" . $readyTimeMinutes . " " . $timeSelect"));  //convert time to 24hr
											echo "<input type='hidden' name='ready-date' value='$ready_date'>";
											echo "<input type='hidden' name='ready-time' value='$ready_time'>";
											echo "<input type='hidden' name='package-type' value='$package_type'>";
											echo "<input type='hidden' name='box-or-bag' value='$boxorbag'>";
											echo "<input type='hidden' name='envelope' value='$envelope'>";
											echo "<input type='hidden' name='other' value='$other'>";
											echo "<input type='hidden' name='comments' value='$comments'>";
									?>
							<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
							<p></p>
							<table cellspacing="5" align="center">
									<tr>
										<td nowrap><label>Ready Date:</label></td>
										<td width="100%"><? echo $ready_date; ?></td>
									</tr>
										<tr>
										<td nowrap><label>Ready Time:</label></td>
										<td>
											<? echo $ready_time; ?>
										</td>
									</tr>
									<tr>
										<td nowrap><label>Package Type:</label></td>
										<td width="100%"><? echo $package_type; ?></td>
									</tr>
										<tr>
										<td nowrap><label>Comments:</label></td>
										<td width="100%"><? echo $comments; ?></td>
									</tr>
							</table>
							
														</td>
													
					
							
											
							<td width="23">&nbsp;</td>
							<td width="332" valign="top">
								
							<p></p>
							<h2>And finally...</h2>
							<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
							<p></p>
							
							<table class="formLine" width="100%">
											<td><label>Reference</label></td>
												<td width="100%"><input id="unit" name="reference" type="text" placeholder="optional, for your own internal use"/>
												</td>
											</table>
	
							
							
						</td>
					</tr>
			
				</table>
				
			<div class="orderButton" style="padding:10px;" align="center">
				<a id="orderSubmit" href="#"><span>Place Order</span></a>
				<!-- <input type="button" id="orderSubmit" class="big" value="Looks Good, Let's Go!"/> -->
				<div class="ajax_loading"><img src="<?php bloginfo( 'template_directory' ) ?>/images/ajax-loader.gif" />
				</div>
			</div>
	</div>

	</form>
    </div>
    <?php 	
	$db->close();
	}
}


geko_render_template();
